import boto3
import csv
#opening a session on ec2 client
ec2 = boto3.client('ec2')
#using the csv library to run a for loop within our csv file to grab items in the ImageId row
with open('amis_list.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader: #for loop within our CSV file
        ami_id = row["ImageId"] #adding imageids to the ami_id to use later
        try: #try/except block to keep the program running incase an ami is unable to be deregistered and snapshot deleted
            response = ec2.describe_images(ImageIds=[ami_id]) 
            block_store = response['Images'][0].get('BlockDeviceMappings',[])

            ec2.deregister_image(ImageId=ami_id) #boto3 session to deregister AMi's first so we can delete the snapshots
            print(f'ami {ami_id} has been deregistered successfully')

            for block in block_store: #for loop to delete the snapshots once we deregister the AMI's
                if "Ebs" in block and "SnapshotId" in block['Ebs']:
                    snapshot_id = block['Ebs']['SnapshotId']
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(f'The {snapshot_id} Snapshot has been successfully deleted')
        except Exception as e:
            print(f"Unable to process {ami_id} AMI: {str(e)} ")

