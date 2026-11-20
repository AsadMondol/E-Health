import boto3
import os
from botocore.exceptions import NoCredentialsError

# AWS SDK uses its standard credential provider chain (environment, profile, IAM role).
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)

def create_table():
    table_schema = {
        'TableName': 'TestingResults',
        'KeySchema': [
            {
                'AttributeName': 'DiseaseName',
                'KeyType': 'HASH'
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'DiseaseName',
                'AttributeType': 'S'
            }
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    
    dynamodb.create_table(**table_schema)

def store_test_results(disease_name, symptoms, medication):
    try:
        dynamodb.describe_table(TableName='TestingResults')
    except dynamodb.exceptions.ResourceNotFoundException:
        create_table()

    dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)

    table = dynamodb_resource.Table('TestingResults')

    item = {
        'DiseaseName': disease_name,
        'Symptoms': symptoms,
        'Medication': medication
    }

    if not disease_name:
        raise ValueError("DiseaseName cannot be empty")

    table.put_item(Item=item)
