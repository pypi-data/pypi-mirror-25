# container-service-extension
# Copyright (c) 2017 VMware, Inc. All Rights Reserved.
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import print_function
import click
import hashlib
import logging
import os
import pika
from pyvcloud.vcd.client import BasicLoginCredentials
from pyvcloud.vcd.client import Client
from pyvcloud.vcd.org import Org
from pyvcloud.vcd.vsphere import VSphere
import requests
import sys
import yaml


LOGGER = logging.getLogger(__name__)
BUF_SIZE = 65536


def generate_sample_config():
    sample_config = """
amqp:
    host: amqp.vmware.com
    port: 5672
    user: 'guest'
    password: 'guest'
    exchange: vcdext
    routing_key: cse

vcd:
    host: vcd.vmware.com
    port: 443
    username: 'administrator'
    password: 'my_secret_password'
    api_version: '6.0'
    verify: False
    log: True

vcs:
    host: vcenter.vmware.com
    port: 443
    username: 'administrator@vsphere.local'
    password: 'my_secret_password'
    verify: False

service:
    listeners: 2
    logging_level: 5
    logging_format: %s

broker:
    type: default
    org: org1
    vdc: vdc1
    catalog: cse
    source_ova: https://bintray.com/vmware/photon/download_file?file_path=photon-custom-hw11-1.0-62c543d.ova
    sha1_ova: 18c1a6d31545b757d897c61a0c3cc0e54d8aeeba
    master_template: k8s-u.ova
    node_template: k8s-u.ova
    username: cse
    password: 'template-password'
    ssh_public_key: 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDFS5HL4CBlWrZscohhqdVwUa815Pi3NaCijfdvs0xCNF2oP458Xb3qYdEmuFWgtl3kEM4hR60/Tzk7qr3dmAfY7GPqdGhQsZEnvUJq0bfDAh0KqhdrqiIqx9zlKWnR65gl/u7Qkck2jiKkqjfxZwmJcuVCu+zQZCRC80XKwpyOudLKd/zJz9tzJxJ7+yltu9rNdshCEfP+OR1QoY2hFRH1qaDHTIbDdlF/m0FavapH7+ScufOY/HNSSYH7/SchsxK3zywOwGV1e1z//HHYaj19A3UiNdOqLkitKxFQrtSyDfClZ/0SwaVxh4jqrKuJ5NT1fbN2bpDWMgffzD9WWWZbDvtYQnl+dBjDnzBZGo8miJ87lYiYH9N9kQfxXkkyPziAjWj8KZ8bYQWJrEQennFzsbbreE8NtjsM059RXz0kRGeKs82rHf0mTZltokAHjoO5GmBZb8sZTdZyjfo0PTgaNCENe0brDTrAomM99LhW2sJ5ZjK7SIqpWFaU+P+qgj4s88btCPGSqnh0Fea1foSo5G57l5YvfYpJalW0IeiynrO7TRuxEVV58DJNbYyMCvcZutuyvNq0OpEQYXRM2vMLQX3ZX3YhHMTlSXXcriqvhOJ7aoNae5aiPSlXvgFi/wP1x1aGYMEsiqrjNnrflGk9pIqniXsJ/9TFwRh9m4GktQ== cse'
    master_cpu: 2
    master_mem: 2048
    node_cpu: 2
    node_mem: 2048

    """ % '%(levelname) -8s %(asctime)s %(name) -40s %(funcName) ' \
          '-35s %(lineno) -5d: %(message)s'
    return sample_config.strip() + '\n'


def bool_to_msg(value):
    if value:
        return 'success'
    else:
        return 'fail'


def get_config(file_name):
    config = {}
    with open(file_name, 'r') as f:
        config = yaml.load(f)
    if not config['vcd']['verify']:
        click.secho('InsecureRequestWarning: '
                    'Unverified HTTPS request is being made. '
                    'Adding certificate verification is strongly '
                    'advised.', fg='yellow', err=True)
        requests.packages.urllib3.disable_warnings()
    return config


def check_config(file_name):
    config = get_config(file_name)
    amqp = config['amqp']
    credentials = pika.PlainCredentials(amqp['user'], amqp['password'])
    parameters = pika.ConnectionParameters(amqp['host'], amqp['port'],
                                           '/',
                                           credentials)
    connection = pika.BlockingConnection(parameters)
    click.echo('Connection to AMQP server (%s:%s): %s' % (amqp['host'],
               amqp['port'],
               bool_to_msg(connection.is_open)))
    connection.close()
    if not config['vcd']['verify']:
        click.secho('InsecureRequestWarning: '
                    'Unverified HTTPS request is being made. '
                    'Adding certificate verification is strongly '
                    'advised.', fg='yellow', err=True)
        requests.packages.urllib3.disable_warnings()
    client = Client(config['vcd']['host'],
                    api_version=config['vcd']['api_version'],
                    verify_ssl_certs=config['vcd']['verify'],
                    log_file='cse.log',
                    log_headers=True,
                    log_bodies=True
                    )
    client.set_credentials(BasicLoginCredentials(config['vcd']['username'],
                                                 'System',
                                                 config['vcd']['password']))
    click.echo('Connection to vCloud Director as system '
               'administrator (%s:%s): %s' %
               (config['vcd']['host'], config['vcd']['port'],
                bool_to_msg(True)))

    if config['broker']['type'] == 'default':
        logged_in_org = client.get_org()
        org = Org(client, org_resource=logged_in_org)
        org.get_catalog(config['broker']['catalog'])
        click.echo('Find catalog \'%s\': %s' %
                   (config['broker']['catalog'], bool_to_msg(True)))
        org.get_catalog_item(config['broker']['catalog'],
                             config['broker']['master_template'])
        click.echo('Find master template \'%s\': %s' %
                   (config['broker']['master_template'], bool_to_msg(True)))
        org.get_catalog_item(config['broker']['catalog'],
                             config['broker']['node_template'])
        click.echo('Find node template \'%s\': %s' %
                   (config['broker']['node_template'], bool_to_msg(True)))

    v = VSphere(config['vcs']['host'],
                config['vcs']['username'],
                config['vcs']['password'],
                port=int(config['vcs']['port']))
    v.connect()
    click.echo('Connection to vCenter Server as %s '
               '(%s:%s): %s' %
               (config['vcs']['username'],
                config['vcs']['host'],
                config['vcs']['port'],
                bool_to_msg(True)))
    return config

def configure_vcd(file_name):
    click.secho('Configuring vCD from file: %s' % file_name)
    config = get_config(file_name)
    client = Client(config['vcd']['host'],
                    api_version=config['vcd']['api_version'],
                    verify_ssl_certs=config['vcd']['verify'],
                    log_file='cse.log',
                    log_headers=True,
                    log_bodies=True
                    )
    client.set_credentials(BasicLoginCredentials(config['vcd']['username'],
                                                 'System',
                                                 config['vcd']['password']))
    click.echo('Connection to vCloud Director as system '
               'administrator (%s:%s): %s' %
               (config['vcd']['host'], config['vcd']['port'],
                bool_to_msg(True)))
    if config['broker']['type'] == 'default':
        orgs = client.get_org_list()
        result = []
        for org in [o for o in orgs.Org if hasattr(orgs, 'Org')]:
            if org.get('name') == config['broker']['org']:
                org_href = org.get('href')
        org = Org(client, org_href=org_href)
        click.echo('Find org \'%s\': %s' %
                   (org.get_name(), bool_to_msg(True)))
        vdc = org.get_vdc(config['broker']['vdc'])
        click.echo('Find vdc \'%s\': %s' %
                   (vdc.get('name'), bool_to_msg(True)))
        try:
            catalog = org.get_catalog(config['broker']['catalog'])
        except:
            catalog = org.create_catalog(config['broker']['catalog'],
                                         'CSE catalog')
            org.share_catalog(config['broker']['catalog'])
        click.echo('Find catalog \'%s\': %s' %
                   (config['broker']['catalog'],
                    bool_to_msg(catalog is not None)))
        try:
            master_template = org.get_catalog_item(config['broker']['catalog'],
                config['broker']['master_template'])
        except:
            master_template = create_master_template(config,
                                                     client,
                                                     org,
                                                     vdc,
                                                     catalog)
        click.echo('Find master template \'%s\': %s' %
                   (config['broker']['master_template'],
                    bool_to_msg(master_template is not None)))

def get_sha1(file):
    sha1 = hashlib.sha1()
    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def upload_source_ova(config, client, org, catalog):
    cse_cache_dir = os.path.join(os.getcwd(), 'cse_cache')
    cse_ova_file = os.path.join(cse_cache_dir,
                                config['broker']['source_ova_name'])
    if not os.path.exists(cse_ova_file):
        if not os.path.isdir(cse_cache_dir):
            os.makedirs(cse_cache_dir)
        click.secho('Downloading %s' % config['broker']['source_ova'],
                    fg='green')
        r = requests.get(config['broker']['source_ova'], stream=True)
        with open(cse_ova_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    if os.path.exists(cse_ova_file):
        sha1 = get_sha1(cse_ova_file)
        assert sha1 == config['broker']['sha1_ova']
        click.secho('Uploading %s' % config['broker']['source_ova_name'],
                    fg='green')
        bytes_written = org.upload_ovf(config['broker']['catalog'],
                                       cse_ova_file,
                                       config['broker']['source_ova_name'],
                                       callback=None)

        return org.get_catalog_item(config['broker']['catalog'],
                                    config['broker']['source_ova_name'])
    else:
        return None

def create_master_template(config, client, org, vdc, catalog):
    try:
        source_ova_item = org.get_catalog_item(config['broker']['catalog'],
            config['broker']['source_ova_name'])
    except:
        source_ova_item = upload_source_ova(config, client, org, catalog)
    click.secho('Find source ova \'%s\': %s' %
                (config['broker']['source_ova_name'],
                 bool_to_msg(source_ova_item is not None)))
    if source_ova_item is not None:
        print(source_ova_item.get('name'))
    else:
        print('not found')
