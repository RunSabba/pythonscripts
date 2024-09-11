import os
from dotenv import load_dotenv
import boto3
load_dotenv()

#crerating an ec2 using a ec2 resource
ec2_resource = boto3.resource("ec2")
my_instance = "RunSabba Cloud"

#variable for my key_pair
EC2_key = os.getenv('EC2_KEY')
#variable for my bashscript installing nginx and my webserver, *add 3 quotes for script*
nginx_script = 



nginx_instance = ec2_resource.create_instances(
    ImageId="ami-0e86e20dae9224db8",
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName=EC2_key,
    UserData=nginx_script,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': 'MyEC2Instance'},]
        },
    ]
)

print("The",nginx_instance[0].id," instance has been created.")