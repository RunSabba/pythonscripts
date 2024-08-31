#Python script used to get a list of my AMI's in boto3 and save themn to a csv file with speficied columns
import boto3
import csv
#opening a session with ec2 client
ec2 = boto3.client('ec2')
#putting the list of images of our aws ["self"] account into the response variable
response = ec2.describe_images(Owners=['self'])
#using the csv lib to open a csv file. using ImageId, Name and CreationDate as columns to list ami info.
with open('amis_list.csv', 'w' , newline='') as csvfile:
    fieldnames = ['ImageId', 'Name', 'CreationDate']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#using the csv library to add the ImageId, Name and CreationDate we grab from iterating thru the for loop.
    writer.writeheader()
    for image in response["Images"]:
        writer.writerow({
            'ImageId': image['ImageId'],
            'Name': image.get('Name'),
            'CreationDate': image['CreationDate']
        })

print(" AMI's are listed in the amis_list.csv file ")
