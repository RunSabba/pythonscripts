#https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/service-resource/instances.html
import boto3
#we can change this if we need to stop instances in other regions
region = "us-east-1"

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
    team_name = "Runsabba-CloudOps"
    tag_filter = {"Name": "tag:Owner", "Values":[team_name]}
    instances = list(ec2_instance.instances.filter(Filters=[tag_filter]))
#updated loop to catch errors and to also added else block to inform us if theres no ec2's to delete(no match in Filter)
    if instances:
        for instance in instances:
            try:
                instance.stop()
                print(f"Stopping CloudOps Instance: {instance.id} ")
            except Exception as e:
                print(f"Error stopping instance {instance.id}: {e}")#if error occurs the mesasage will be stored in "e" as a variable"
    else:
        print(f"There are no ec2's to delete for {team_name} ")


stop_cloudops_instances()    
