import boto3
import requests
import json
import os

# Constants for AWS access, replace with your actual details
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
HOSTED_ZONE_ID = os.getenv('HOSTED_ZONE_ID')

def get_public_ip():
    response = requests.get("http://checkip.amazonaws.com/")
    return response.text.strip()

def load_ip_data():
    with open('subdomainlist.json', 'r') as file:
        return json.load(file)

def save_ip_data(ip_data):
    with open('subdomainlist.json', 'w') as file:
        json.dump(ip_data, file, indent=4)

def fetch_route53_records(client):
    records = []
    full_record_sets = []  # To store full record data

    paginator = client.get_paginator('list_resource_record_sets')
    source_zone_records = paginator.paginate(HostedZoneId=HOSTED_ZONE_ID)

    for record_set in source_zone_records:
        for record in record_set['ResourceRecordSets']:
            if record['Type'] == 'A':  # We are only interested in 'A' records
                records.append(record['Name'][:-1])  # Removing trailing dot
                full_record_sets.append(record)  # Storing full record

    return records, full_record_sets

def sync_route53_records(client, current_ip, domain_list, current_records, all_record_sets):
    changes = []

    # Map the record sets for easier access
    record_set_map = {record['Name'][:-1]: record for record in all_record_sets if record['Type'] == 'A'}

    # Records to DELETE: They are in Route53 but not in our domain list
    for domain in current_records:
        if domain not in domain_list:
            record_data = record_set_map.get(domain)  # Fetch the current record data
            if record_data:
                changes.append({
                    'Action': 'DELETE',
                    'ResourceRecordSet': record_data  # Use actual current record data
                })

    # Records to UPSERT: They are in our domain list (regardless of their presence in Route53)
    for domain in domain_list:
        changes.append({
            'Action': 'UPSERT',
            'ResourceRecordSet': {
                'Name': f'{domain}.',  # Adding trailing dot, required by AWS
                'Type': 'A',
                'TTL': 300,
                'ResourceRecords': [{'Value': current_ip}]
            }
        })

    # Applying changes if the list is not empty
    if changes:
        response = client.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch={'Changes': changes}
        )
        return response

    return None

