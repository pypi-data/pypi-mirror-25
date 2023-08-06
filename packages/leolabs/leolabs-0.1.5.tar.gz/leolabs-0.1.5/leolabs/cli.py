#!/usr/bin/env python

import os, sys
import traceback
from collections import defaultdict
import argparse
import json

def quit(message):
    sys.stderr.write(message + '\n')
    sys.exit(1)

try:
    import requests
except:
    quit('Failed to import requests library. Try "pip install requests"')


access_key = os.environ.get('LEOLABS_ACCESS_KEY')
secret_key = os.environ.get('LEOLABS_SECRET_KEY')
if not access_key or not secret_key:
    quit('Missing LeoLabs credentials. Please set the LEOLABS_ACCESS_KEY and LEOLABS_SECRET_KEY environment variables.')


def api_request(resource, data=None):
    base_uri = os.environ.get('LEOLABS_BASE_URI', 'https://api.leolabs.space/v1')
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

def catalog_search(norad_catalog_number):
    resource = '/catalog/objects/search?noradCatalogNumber={0}'.format(norad_catalog_number)
    response = api_request(resource)
    if response and 'catalogNumber' in response:
        return response
    return None

def catalog_create_task(catalog_number, start_time, end_time):
    if catalog_number and catalog_number[0] != 'L':
        search_results = catalog_search(catalog_number)
        if search_results:
            catalog_number = search_results['catalogNumber']

    resource = '/catalog/objects/{0}/tasks'.format(catalog_number)
    response = api_request(resource, data={'startTime': start_time, 'endTime': end_time, 'priority': 100})
    return response

class Command:
    def __init__(self, resource, command, function):
        self.resource = resource
        self.command = command
        self.function = function

    def invoke(self, args):
        return json.dumps(self.function(*args), indent=4)

class CommandList:
    def __init__(self):
        self.commands = defaultdict(defaultdict)

    def add(self, command):
        self.commands[command.resource][command.command] = command

    def invoke(self, resource, command, args):
        if resource not in self.commands:
            sys.stderr.write('Did not recognize resource: {0}, valid choices are: {1}\n'.format(resource, self.commands.keys()))
            sys.exit(1)

        if command not in self.commands[resource]:
            sys.stderr.write('Did not recognize command {0} for resource {1}, valid choices are: {2}\n'.format(command, resource, self.commands[resource].keys()))
            sys.exit(1)

        print(self.commands[resource][command].invoke(args))


def main():

    parser = argparse.ArgumentParser(description='LeoLabs Command Line Interface')
    parser.add_argument('resource')
    parser.add_argument('command')
    parser.add_argument('remaining', nargs='*')
    args = parser.parse_args()

    resource = args.resource
    command = args.command
    remaining_args = args.remaining

    commands = CommandList()
    commands.add(Command('catalog', 'search', catalog_search))
    commands.add(Command('catalog', 'create-task', catalog_create_task))


    commands.invoke(resource, command, remaining_args)

if __name__ == '__main__':
    main()