import boto3
import os
from pprint import pprint

client = boto3.client(
    service_name='bedrock',
    aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='us-west-2')
response = client.list_foundation_models(byProvider='string',
                                         byOutputModality='EMBEDDING',
                                         byInferenceType='ON_DEMAND')
pprint(response['modelSummaries'])
