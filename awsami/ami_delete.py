import boto3
import csv
#opening a session on ec2 client
ec2 = boto3.client('ec2')
#this will open my amis_list.csv file, the with statement will close file once we're done.
with open('amis_list.csv', newline='') as csvfile:
    #this will read my csv file as a dictionary.
    reader = csv.DictReader(csvfile)
    for row in reader: #for loop iterates over each row in my csv file.
        ami_id = row["ImageId"] #this will extract the AMI ID from each row.
        try: #try/except block to keep the program running incase an ami is unable to be deregistered and snapshot deleted
            response = ec2.describe_images(ImageIds=[ami_id]) #this will use the boto3 client to grab the details of the AMI
            block_store = response['Images'][0].get('BlockDeviceMappings',[])#this will grab the block device mappings of the ami, this will contain the snapshot associated with the AMI

            ec2.deregister_image(ImageId=ami_id) #boto3 session to deregister AMi's using the AMI ID first so we can delete the snapshots
            print(f'ami {ami_id} has been deregistered successfully')

            for block in block_store: #this will iterate over the block device mappings in the block_store variable.
                if "Ebs" in block and "SnapshotId" in block['Ebs']:# checks if the block device has an EBS vol associated, then to see if that same EBS has a snapshot associated.
                    snapshot_id = block['Ebs']['SnapshotId']#extracts the snapshot ID from the EBS volume.
                    ec2.delete_snapshot(SnapshotId=snapshot_id)#deletes the snapshot
                    print(f'The {snapshot_id} Snapshot has been successfully deleted')
        except Exception as e:
            print(f"Unable to process {ami_id} AMI: {str(e)} ")

