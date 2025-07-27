import json 
import boto3 # SDK for python. Allows the use of Python to interact with AWS resources 
import gzip 
import base64
from datetime import datetime

s3 = boto3.client("s3") # helps create a connection to AWS S3 and provides methods to interact with S3 buckets and objects 
bucket_name = "ryan-siem-logs"

def lambda_handler(event, context):
    cloudwatch_data = event["awslogs"]["data"] # nested dictionary to access keys, like "person['address]['street']"
    compressed_payload = base64.b64decode(cloudwatch_data) # Cloudwatch Logs initially compresses the payload for every log. This decodes it (base64 --> binary) to use less bandwidth
    uncompressed_payload = gzip.decompress(compressed_payload) # This decompresses the file (gzip --> readable text) to work with original compressed data
    log_events = json.loads(uncompressed_payload) # takes original data from JSON format into a python dictionary to access data "log_events['logEvents]"

    log_entries = []

    for event in log_events["logEvents"]:
        message = event["message"]
        log_entries.append(message)
        
    if log_entries:
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S")
        key = f"logs/ssh_attempts_{timestamp}.log"
        body = "\n".join(log_entries)

        s3.put_object(Bucket="ryan-siem-logs", Key=key, Body=body.encode("utf-8")) # converts string to bytes since S3 requires binary data

    return {
        "statusCode": 200, # HTTP status code success/OK
        "body": json.dumps("Logs successfully uploaded to Amazon S3")
    }