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

    obj_dict = s3.list_objects(Bucket = S3Bucket)
    obj = obj_dict['Contents']
    for i in range(0,len(obj)):
        if threshold_dt >= obj[i]['LastModified'].strftime('%Y-%m-%d') :
            obj_name = obj[i]['Key']
            res = s3.delete_object(Bucket = S3Bucket, Key = obj_name)
            del_file_list.append(obj_name)
            del_counter += 1

    del_file_str = str(del_file_list).strip('[]')
    if del_counter > 0:
        print(str(del_counter) + " files which were created on or before the threshold date of - " + threshold_dt + " have been deleted. Here are their names - " + del_file_str)
    else:
        print("No files were created on or before " + threshold_dt + ", hence none deleted.")
    return "Process completed successfully."
