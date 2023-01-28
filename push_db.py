import boto3
import os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()
print('dynamodb connected!!....')
dynamodb = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
    'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]
# if 'Content_Analysis' not in existing_tables:
#     dynamodb.create_table(
#         TableName='Content_Analysis',
#         KeySchema=[
#             {
#                 'AttributeName': 'Date',
#                 'KeyType': 'HASH'  # Partition key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'Date',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
#     print('create table Content_Analysis')
# if 'User_Master' not in existing_tables:
#     dynamodb.create_table(
#         TableName='User_Master',
#         KeySchema=[
#             {
#                 'AttributeName': 'User_ID',
#                 'KeyType': 'HASH'  # Partition key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'User_ID',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
#     print('create table User_Master')
# if 'Telegram_Master' not in existing_tables:
#     dynamodb.create_table(
#         TableName='Telegram_Master',
#         KeySchema=[
#             {
#                 'AttributeName': 'ID',
#                 'KeyType': 'HASH'  # Partition key
#             }
#         ],
#         AttributeDefinitions=[
#             {
#                 'AttributeName': 'ID',
#                 'AttributeType': 'S'
#             }
#         ],
#         ProvisionedThroughput={
#             'ReadCapacityUnits': 10,
#             'WriteCapacityUnits': 10
#         }
#     )
# print('create table Telegram_Master')
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
    print('create table WCB_Data')
