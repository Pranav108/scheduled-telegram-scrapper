import boto3
import os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()
print('dynamodb connected!!....')
dynamodb = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
    'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]

if 'ST_Content_Analysis' not in existing_tables:
    dynamodb.create_table(
        TableName='ST_Content_Analysis',
        KeySchema=[
            {
                'AttributeName': 'Timing',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Timing',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table ST_Content_Analysis')
    
if 'ST_User_Master' not in existing_tables:
    dynamodb.create_table(
        TableName='ST_User_Master',
        KeySchema=[
            {
                'AttributeName': 'User_ID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_ID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table ST_User_Master')
    
if 'ST_User_Data' not in existing_tables:
    dynamodb.create_table(
        TableName='ST_User_Data',
        KeySchema=[
            {
                'AttributeName': 'ID',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'ID',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table ST_User_Data')
    
if 'ST_Telegram_Master' not in existing_tables:
    dynamodb.create_table(
        TableName='ST_Telegram_Master',
        KeySchema=[
            {
                'AttributeName': 'Date',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table ST_Telegram_Master')

if 'ST_WCB_Data' not in existing_tables:
    dynamodb.create_table(
        TableName='ST_WCB_Data',
        KeySchema=[
            {
                'AttributeName': 'Datetime',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Datetime',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table ST_WCB_Data')