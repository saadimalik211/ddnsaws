import json

# Load the subdomain list
with open('subdomainlist.json', 'r') as file:
    subdomains = json.load(file)

# Load the acme.json file
with open('acme.json', 'r') as file:
    acme_data = json.load(file)

# Extract the list of domains from subdomains
valid_domains = set(subdomains.keys())

# Filter the certificates in acme.json to only include valid domains
valid_certificates = [
    cert for cert in acme_data['lets-encrypt']['Certificates']
    if cert['domain']['main'] in valid_domains
]

# Replace the certificates in the acme_data with the filtered certificates
acme_data['lets-encrypt']['Certificates'] = valid_certificates

# Save the cleaned acme.json
with open('acme_cleaned.json', 'w') as file:
    json.dump(acme_data, file, indent=2)

print("Cleaned acme.json saved as acme_cleaned.json")

