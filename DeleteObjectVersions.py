import json
import boto3
import os
from datetime import datetime, timedelta

s3 = boto3.client('s3')
RetentionPeriod = int(os.getenv('RetentionPeriod'))
S3Bucket = os.getenv('S3Bucket')

def lambda_handler(event, context):
    del_counter = 0 # Initializing a counter to count the number of files being deleted
    del_file_list = [] # Initializing an empty list to store the file & version which are deleted
    threshold_dt = (datetime.today() - timedelta(days=RetentionPeriod)).strftime('%Y-%m-%d') # Getting the date for previous date

    obj = s3.list_object_versions(Bucket = S3Bucket)
    for i in range(0,len(obj.keys())):
        if threshold_dt >= obj['Versions'][i]['LastModified'].strftime('%Y-%m-%d') :
            obj_name = obj['Versions'][i]['Key']
            obj_ver = obj['Versions'][i]['VersionId']
            obj_date = obj['Versions'][i]['LastModified']
            res = s3.delete_object(Bucket = S3Bucket, Key = obj_name, VersionId = obj_ver)
            del_file_list.append(obj_name + " " + obj_ver)
            del_counter += 1
            del_file_str = str(del_file_list).strip('[]')
    print(str(del_counter) + " files which were created on or before the threshold date of - " + threshold_dt + " have been deleted. Here are their names & version ids - " + del_file_str)
    return "Process completed successfully."
