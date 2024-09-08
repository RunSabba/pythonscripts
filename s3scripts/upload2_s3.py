#script to upload/update/read files on s3 buckets using boto3
import boto3

s3 = boto3.resource("s3")
bucket = "runsabba-docker"

#two different docker files. Dfile_1: python:3.6 Dfile_2 python:3.6-alpine
Dfile_1 = "Dockerfile1"
Dfile_2 = "Dockerfile2"

#this line will grab the bucket variable and upload the file to the bucket.
s3.Bucket(bucket).upload_file(Filename=Dfile_1, Key=Dfile_1)
# funtion to add objects to my bucket.
def bucket_manipulation():
    #s3.Object will add my s3 bucket and object within the object variable.
    object = s3.Object(bucket, Dfile_1)
    #object.get will grab the object withi my bucket and will be placed in the bucket_output variable.
    bucket_output = object.get()['Body'].read()
    #print the object (duckerfile1)
    print(bucket_output)
bucket_manipulation()

#using the .put method to open Body(file) and replace with Dfile_2 content
s3.Object(bucket, Dfile_1).put(Body=open(Dfile_2, 'rb'))

#calling the funtion to print the contents.
bucket_manipulation()

#deleteing the objects within the bucket. cannot delete a bucket with objects.
s3.Object(bucket, Dfile_1).delete()

bucket_name = s3.Bucket(bucket)
bucket_name.delete()
