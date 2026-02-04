import argparse
from jinja2 import Environment, FileSystemLoader
import os
import requests
import sys
from pprint import pprint

parser = argparse.ArgumentParser(description='Build Ansible Vars from GraphQL')
parser.add_argument('-b', '--branch', type=str, help='Infrahub branch', required=True)
parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
args = parser.parse_args()

INFRAHUB_ADDRESS = os.environ.get("INFRAHUB_ADDRESS")
url = f'{INFRAHUB_ADDRESS}/graphql/{args.branch}'
all_variables = {}

with open('graphql/f5_vip_query.gql', 'r') as fh:
    body = fh.read()

response = requests.post(url=url, json={'query': body})
if response.status_code == 200:
    vips = response.json()['data']['ServiceVIP']['edges']
    if not vips:
        sys.exit(f"No VIPS found in branch {args.branch}")
    if args.verbose:
        print()
        print("Data from Infrahub graphql query:")
        print("---------------------------------")
        pprint(vips)
    # VIPS
    all_variables['vips'] = []
    for vip in vips:
        vip_node = vip['node']
        vip_dict = {
            'name': vip_node['name']['value'],
            'service_port': vip_node['service_port']['value'],
            'source_address': vip_node['source_address']['value'],
            'f5_pool': vip_node['f5_pool']['node']['name']['value'],
            'members': []
        }
        members = vip_node['f5_pool']['node']['member']['edges']
        for member in members:
            member_node = member['node']
            member_dict = {
                'name': member_node['name']['value'],
                'service_port': member_node['service_port']['value'],
                'ip_address': member_node['f5_node']['node']['ip_address']['value'],
                'fqdn': member_node['f5_node']['node']['fqdn']['value'],
                'node_name': member_node['f5_node']['node']['name']['value']
            }
            vip_dict['members'].append(member_dict)
        all_variables['vips'].append(vip_dict)

    if args.verbose:
        print()
        print("Formatted data to render group_vars:")
        print("---------------------------------")
        pprint(all_variables)