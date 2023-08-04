import boto3

s3 = boto3.client('s3')
s3.download_file('test-ifty-boto3', 'test-upload-using-boto3', 'downloading-from-s3')