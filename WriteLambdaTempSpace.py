import json
import os
import boto3

s3_client = boto3.client('s3')
S3Bucket = os.getenv('S3Bucket')
TgtFile = os.getenv('TgtFile')
tgt='/tmp/sample.txt'
num_list=list(range(0,6))
    
def lambda_handler(event, context):

    with open(tgt, "a") as myfile:
        myfile.write("In this program, I'm going to demonstrate how a file can be written recursively via python - " + "\n")
        for num in num_list:
            myfile.write("\t Current number is - " + str(num) + "\n")
            myfile.write("\t\t This is iteration - " + str(num+1) +"\n")
        myfile.write("I hope this exercise was helpful to you.")
    
    s3_client.upload_file(tgt, S3Bucket, TgtFile)
    
    with open(tgt, "r") as f:
        return (f.read())
