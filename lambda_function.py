import json
import boto3
from animal import Animal
from ex import *

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # TODO implement
    cat = Animal()
    cat_sound = cat.meow()
    bucket_list = []
    for bucket in s3.buckets.all():
        print(bucket.name)
        bucket_list.append(bucket.name)
        
    key = ""
    body = ""
    c = 0
    for obj in bucket.objects.all():
        if obj.key == "input1.txt":
            key = obj.key
            body = obj.get()['Body'].read() 
            c += 1
            break
        c += 1
        
    return {
        'statusCode': 200,
        'body': bucket_list,
        'cat_sound': cat_sound,
        'key': key,
        'body_of_file': body,
        'c': c
    }
