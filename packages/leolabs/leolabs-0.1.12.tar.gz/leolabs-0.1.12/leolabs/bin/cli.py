#!/usr/bin/env python

import os, sys
import traceback
from collections import defaultdict
import argparse
import json
import requests

access_key = None
secret_key = None
override_base_uri = None

def quit(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

def api_request(resource, data=None):

    require_credentials()

    global override_base_uri
    if not override_base_uri:
        base_uri = 'https://api.leolabs.space/v1'
    else:
        base_uri = override_base_uri

    uri = base_uri + resource

    headers = {
        'Authorization': 'basic {0}:{1}'.format(access_key, secret_key)
    }

    for retry in range(5):
        if data is None:
            response = requests.get(uri, headers=headers)
        else:
            response = requests.post(uri, headers=headers, data=data)

        if response.status_code >= 200 and response.status_code <= 399:
            return response.json()

    sys.stderr.write('Request failed with code {0} after retries: "{1}"\n'.format(response.status_code, uri))
    return None

def catalog_search(norad_catalog_number=None, **kwargs):
    resource = '/catalog/objects/search?noradCatalogNumber={0}'.format(norad_catalog_number)
    response = api_request(resource)
    if response and 'catalogNumber' in response:
        return response
    return None

def catalog_create_task(catalog_number=None, norad_catalog_number=None, start_time=None, end_time=None, **kwargs):

    # transparently handle norad catalog number if that is passed instead
    if norad_catalog_number:
        catalog_number = norad_catalog_number
    if catalog_number and catalog_number[0] != 'L':
        search_results = catalog_search(catalog_number)
        if search_results:
            catalog_number = search_results['catalogNumber']

    resource = '/catalog/objects/{0}/tasks'.format(catalog_number)
    print(resource)
    response = api_request(resource, data={'startTime': start_time, 'endTime': end_time, 'priority': 100})
    return response

class Command:
    def __init__(self, resource, command, function):
        self.resource = resource
        self.command = command
        self.function = function

    def invoke(self, args):
        return json.dumps(self.function(**vars(args)), indent=4)

class CommandList:
    def __init__(self):
        self.commands = defaultdict(defaultdict)

    def add(self, command):
        self.commands[command.resource][command.command] = command

    def invoke(self, args):
        resource = args.resource
        command = args.command

        if resource not in self.commands:
            sys.stderr.write('Did not recognize resource: "{0}", valid choices are: {1}\n'.format(resource if resource else '', self.commands.keys()))
            sys.exit(1)

        if command not in self.commands[resource]:
            sys.stderr.write('Did not recognize command "{0}" for resource "{1}", valid choices are: {2}\n'.format(command if command else '', resource, self.commands[resource].keys()))
            sys.exit(1)

        print(self.commands[resource][command].invoke(args))


def import_configparser():
    """ Python 2 + 3 compatibility bridge """
    if sys.version_info[0] < 3:
      import ConfigParser
      configparser = ConfigParser
    else:
      import configparser
    return configparser


def configure(**kwargs):
    configparser = import_configparser()

    from os.path import expanduser
    home_dir = expanduser("~")
    leolabs_dir = os.path.join(home_dir, '.leolabs')

    try:
      os.makedirs(leolabs_dir)
    except:
      pass

    config_path = os.path.join(leolabs_dir, 'config')

    def prompt(s):
      if sys.version_info[0] < 3:
        return raw_input(s)
      else:
        return input(s)

    access_key = prompt('Access Key: ')
    secret_key = prompt('Secret Key: ')

    config = configparser.ConfigParser()
    config.add_section('credentials')
    config.set('credentials', 'access_key', access_key)
    config.set('credentials', 'secret_key', secret_key)

    with open(config_path, 'w') as f:
      config.write(f)

def load_config():

    global access_key, secret_key, override_base_uri

    if access_key and secret_key:
        return

    access_key = os.environ.get('LEOLABS_ACCESS_KEY')
    secret_key = os.environ.get('LEOLABS_SECRET_KEY')
    override_base_uri = os.environ.get('LEOLABS_BASE_URI')

    if access_key and secret_key:
        return

    configparser = import_configparser()

    from os.path import expanduser
    home_dir = expanduser("~")
    leolabs_dir = os.path.join(home_dir, '.leolabs')
    config_path = os.path.join(leolabs_dir, 'config')

    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        access_key = config.get('credentials', 'access_key')
        secret_key = config.get('credentials', 'secret_key')
        override_base_uri = config.get('default', 'base_uri')

        if access_key and secret_key:
            return
    except:
        pass


def require_credentials():    
    if not access_key or not secret_key:
        quit('Missing LeoLabs credentials. Please set the LEOLABS_ACCESS_KEY and LEOLABS_SECRET_KEY environment variables, or run "leolabs configure".')

def main():

    load_config()

    parser = argparse.ArgumentParser(description='LeoLabs Command Line Interface')
    parser.add_argument('resource', nargs='?')
    parser.add_argument('command', nargs='?')
    parser.add_argument('--catalog-number', dest='catalog_number')
    parser.add_argument('--norad-catalog-number', dest='norad_catalog_number')
    parser.add_argument('--state', dest='state')
    parser.add_argument('--instrument', dest='instrument')
    parser.add_argument('--task', dest='task')
    parser.add_argument('--latest', dest='latest')
    parser.add_argument('--start-time', dest='start_time')
    parser.add_argument('--end-time', dest='end_time')
    args = parser.parse_args()

    commands = CommandList()
    commands.add(Command('configure', None, configure))
    commands.add(Command('catalog', 'search', catalog_search))
    commands.add(Command('catalog', 'create-task', catalog_create_task))

    commands.invoke(args)

if __name__ == '__main__':
    main()