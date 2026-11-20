import boto3
import os
from botocore.exceptions import NoCredentialsError

# AWS credentials
AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')

# Initialize DynamoDB client with credentials
try:
    dynamodb = boto3.client('dynamodb', region_name=AWS_REGION)
except NoCredentialsError:
    print("AWS credentials not found. Please provide valid credentials.")

def create_table():
    # Define the table schema
    table_schema = {
        'TableName': 'TestingResults',
        'KeySchema': [
            {
                'AttributeName': 'DiseaseName',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        'AttributeDefinitions': [
            {
                'AttributeName': 'DiseaseName',
                'AttributeType': 'S'  # String
            }
        ],
        # Specify provisioned capacity to stay within Free Tier limits
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    }
    
    # Create the table
    dynamodb.create_table(**table_schema)

def store_test_results(disease_name, symptoms, medication):
    # Check if the table exists, if not, create it
    try:
        dynamodb.describe_table(TableName='TestingResults')
    except dynamodb.exceptions.ResourceNotFoundException:
        create_table()

    # Initialize DynamoDB resource
    dynamodb_resource = boto3.resource('dynamodb', region_name=AWS_REGION)

    # Get the table
    table = dynamodb_resource.Table('TestingResults')

    # Prepare item to be stored in the table
    item = {
        'DiseaseName': disease_name,
        'Symptoms': symptoms,
        'Medication': medication
    }

    # Store the item in the table
    table.put_item(Item=item)
    print("Test results stored successfully.")

# Example usage
disease_name = "Chikungunya"
symptoms = ["Joint pain", "Headache", "Muscle pain", "Joint swelling", "Rash"]
medication = ["Americas", "Asia", "Europe", "Caribbean"]

# Store test results in DynamoDB
store_test_results(disease_name, symptoms, medication)
