#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html
import boto3
#we can change this if we need to stop instances in other regions
region = "us-west-2"

#creating the connection with ec2 thru boto3
ec2_instance = boto3.resource('ec2',region_name=region)

def stop_all_instances():
#for loop to interate thru the ec2's in my account and stop them. 
    for instances in ec2_instance.instances.all():
        instances.stop()
    print("Stopping instances..")    

#improve on this tomorrow

def stop_cloudops_instances():
#This will filter out my prod servers by tags to shut off specific servers upon command.
    prod_filter = {"Name": "tag:Owner", "Values":["Runsabba-Test"]}
#for loop will iterate thru ec2's and we will stop instances that meet the tag name and values
    for instances in ec2_instance.instances.filter(Filters=[prod_filter]):
        instances.stop()
    print("Stopping CloudOps Instances..")  

stop_cloudops_instances()    
