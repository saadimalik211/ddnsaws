--------------------------------------------------------------------------------
#                         Dynamic DNS Using AWS Route 53 (ddnsaws)
--------------------------------------------------------------------------------

##DESCRIPTION
-----------
'ddnsaws' is a tool that automates the process of keeping a DNS record updated with a server's most current IP address. This script is especially useful in environments with dynamic public IP addresses. It's Dockerized and uses AWS Boto3 for interacting with AWS services.


##FEATURES
--------
- Automatic IP detection: Regularly checks the public IP address of your server and updates AWS Route 53 if it changes.
- Docker support: The tool is containerized for easy deployment and consistent run environments.
- AWS Boto3 integration: Interacts seamlessly with AWS services, ensuring smooth operation within the AWS ecosystem.
- Error handling and logging: Provides efficient logging mechanisms for easy troubleshooting and operation monitoring.


##PREREQUISITES
-------------
Before you deploy 'ddnsaws', ensure the following requirements are met:

- Docker and Docker Compose are installed on your server.
- An AWS account with the necessary permissions for Route 53 access.
- A domain managed via AWS Route 53.


##SETUP AND DEPLOYMENT
--------------------
###1. Clone the Repository:
   Clone the repository to your local server where Docker and Docker Compose are installed.

   git clone https://your-repository-link.git
   cd path-to-your-cloned-repository

###2. Configuration:
   Configure your AWS credentials and target DNS record:

   - Rename 'ddns.env.example' to 'ddns.env'.
   - Update 'ddns.env' with your AWS credentials and other necessary configurations.

   AWS_ACCESS_KEY_ID=your_access_key_id
   AWS_SECRET_ACCESS_KEY=your_secret_access_key
   AWS_REGION=your_aws_region
   HOSTED_ZONE_ID=your_hosted_zone_id

   Important: Keep your AWS credentials confidential to prevent unauthorized access.

###3. Build and Run with Docker:
   In the project's root directory, use Docker Compose to build and start the service.

   docker-compose build
   docker-compose up -d

   This will launch the service in the background, and it will continue running, periodically checking your server's IP address and updating the DNS records if necessary.


##USAGE
-----
'ddnsaws' is designed to run autonomously. You can, however, monitor its operation through Docker logs and status checks:

   docker-compose logs -f  # Displays log output
   docker-compose ps       # Shows running services

To stop 'ddnsaws', use the following command:

   docker-compose down


##CONTRIBUTING
------------
Contributions to improve 'ddnsaws' are welcomed! Here's how you can contribute:

1. Fork the project.
2. Create a new feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a new Pull Request.

Please ensure your contributions adhere to the existing coding style and functionality.


##LICENSE
-------
Distributed under the MIT License. See 'LICENSE' for more information.


##CONTACT
-------
For issues, questions, or assistance, please use the GitHub issue tracker or contact the maintainers directly.

--------------------------------------------------------------------------------

