import os
import time
from ddnsr53functions import (
    get_public_ip, load_ip_data, save_ip_data, fetch_route53_records, sync_route53_records
)
import boto3

def main():
    while True:  # This script runs indefinitely, checking for changes every 5 minutes.
        try:
            print("Checking current public IP...")  # New log statement
            current_ip = get_public_ip()
            print(f"Current IP: {current_ip}")  # New log statement

            ip_data = load_ip_data()

            if ip_data.get("_current_ip") != current_ip:
                print("IP has changed. Updating Route53 records...")  # New log statement

                # Establish a session with AWS
                session = boto3.Session(
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION_NAME', 'us-east-1')
                )
                client = session.client('route53')

                # Fetch current records from Route53
                print("Fetching current records from Route53...")  # New log statement
                current_records, all_record_sets = fetch_route53_records(client)

                # Extract domain list from ip_data, excluding the special key
                domain_list = [domain for domain in ip_data if domain != "_current_ip"]

                # Sync records in Route53 based on our domain list
                print("Syncing records in Route53...")  # New log statement
                response = sync_route53_records(client, current_ip, domain_list, current_records, all_record_sets)
                print("Records synced. Response:", response)  # New log statement

                # Update the saved IP data
                for domain in domain_list:
                    ip_data[domain] = current_ip

                ip_data["_current_ip"] = current_ip  # Update the current IP
                save_ip_data(ip_data)

            else:
                print("IP has not changed.")  # New log statement

            print("Sleeping for 5 minutes...")  # New log statement
            time.sleep(300)  # 5-minute interval between checks

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(300)  # If an error occurs, we'll wait for the next cycle

if __name__ == "__main__":
    main()

