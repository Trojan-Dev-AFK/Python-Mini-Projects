import os
import boto3
import time
import csv
import pandas as pd
import numpy as np

os.environ['AWS_PROFILE'] = "default"

client = boto3.client('iam')
def lambda_handler(event, context):
    
    # Generating and fetching the Report
    response = client.generate_credential_report()
    time.sleep(10)
    cred_repot = client.get_credential_report()

    # Decoding because of byte type and converting to basic python dictionary
    content = cred_repot["Content"].decode("utf-8")   
    content_lines = content.split("\n")
    creds_reader = csv.DictReader(content_lines, delimiter=",")
    creds_dict = dict(enumerate(list(creds_reader)))

    # Initialize iterating variables
    header_names = []
    creds_list = []
    iter_count = 0

    # Finding and creating the header row and appending the value rows in seperate list
    for i in creds_dict:
        if (iter_count == 0):
            header_names = list(creds_dict[i].keys())
            creds_list.append(creds_dict[i])
            iter_count += 1
        else:
            creds_list.append(creds_dict[i])
            iter_count += 1
    
    # Saving the report into external .csv file
    with open('Status_report.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = header_names)
        writer.writeheader()
        writer.writerows(creds_list)
    

    # Removing empty rows (Note: 'N/A' values will be converted to null fields)
    df = pd.read_csv('Status_report.csv')
    df.to_csv('Status_report.csv', index=False)

    # Pushing the file to AWS S3 Bucket
    bucket_name = "test-cred-report"
    csv_file_name = "Status_report.csv"
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket = bucket_name,
        Key = csv_file_name
    )

lambda_handler("test", "hello world!")