import boto3
#using ressource to create the bucket thru API call using bot03.
s3 = boto3.resource('s3')
#creating this loop to ensure We can get a unique bucket name and not break out until the user inputs one.
while True:
    bucket = input(" Please enter a unique bucket name: ")

    #bucket.name will tell the for loop to grab the bucket name of each bucket we have in our account and [] puts it into a list which we assign to the my_buckets variable
    my_buckets = [bucket.name for bucket in s3.buckets.all()]
    #if the bucket name is unique it will successfully create the bucket and break the loop (line15), if not the else statement will grab it and we will loop back to the input.
    if bucket not in my_buckets:
        print (f" The {bucket} bucket name is available, creating the S3 bucket... ")
        s3.create_bucket(Bucket=bucket)
        print (f" The {bucket} bucket has been successfully created. " )
        break
    else:
        print (f" The {bucket} bucket name already exists, Please create a unique bucket name. ")    

