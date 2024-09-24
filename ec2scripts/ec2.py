import os
from dotenv import load_dotenv
import boto3
load_dotenv()

#creating an ec2 using a ec2 resource
region_name = "us-east-1"
ami = "ami-0e86e20dae9224db8"
instance_owner = "Runsabba-CloudOps"
ec2_resource = boto3.resource("ec2", region_name = region_name)


#variable for my key_pair
EC2_key = os.getenv('EC2_KEY')
#variable for my bashscript installing nginx and my webserver, *add 3 quotes for script*
nginx_script = '''#!/bin/bash
# Log start of script execution
echo "Starting user data script execution..." > /var/log/user-data.log

# Update packages and install nginx
sudo apt update
sudo apt upgrade -y
sudo apt install nginx -y

# Enable and start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# Create the custom index.html
echo "<html><body><h1>Hello from RunSabba Web Server 1!</h1></body></html>" | sudo tee /var/www/html/index.html

# Log the end of script execution
echo "User data script execution has completed." >> /var/log/user-data.log
'''



nginx_instance = ec2_resource.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=EC2_key,
    UserData=nginx_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'RunSabba Nginx Server'},
                     {'Key': 'Owner', 'Value': instance_owner }]
        },
    ]
)

print(f"The {nginx_instance[0].id} instance has been created in the {region_name} region.")