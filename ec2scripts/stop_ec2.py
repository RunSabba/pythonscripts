import boto3
#creating the connection with ec2 thru boto3
ec2_instance = boto3.resource('ec2')
#for loop to interate thru the ec2's in my account and stop them. 
for instances in ec2_instance.instances.all():
    instances.stop()

#improve on this tomorrow