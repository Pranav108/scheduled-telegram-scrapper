import boto3
import os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()
print('dynamodb connected!!....')
dynamodb = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
    'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]

if 'UAT_Content_Analysis' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_Content_Analysis',
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
    print('create table UAT_Content_Analysis')
    
if 'UAT_User_Master' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_User_Master',
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
    print('create table UAT_User_Master')
    
if 'UAT_User_Data' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_User_Data',
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
    print('create table UAT_User_Data')
    
if 'UAT_Telegram_Master' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_Telegram_Master',
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
    print('create table UAT_Telegram_Master')

if 'UAT_WCB_Data' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_WCB_Data',
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
    print('create table UAT_WCB_Data')
    
if 'UAT_JumbledWord_bank' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_JumbledWord_bank',
        KeySchema=[
            {
                'AttributeName': 'word',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'word',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_JumbledWord_bank')
    
if 'UAT_JumbledWord_Engagement' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_JumbledWord_Engagement',
        KeySchema=[
            {
                'AttributeName': 'Date',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'DateTimeStamp',
                'KeyType': 'RANGE'  #Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Date',
                'AttributeType': 'S'  # Partition key
            },
            {
                'AttributeName': 'DateTimeStamp',
                'AttributeType': 'S'  #Sort key
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_JumbledWord_Engagement')

# ADD INDEX KEY IN THIS TABLE
if 'UAT_QuizBot_Bank' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_QuizBot_Bank',
        KeySchema=[
            {
                'AttributeName': 'quiz_no',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'quiz_no',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_QuizBot_Bank')
    
if 'UAT_QuizBot_Engagement' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_QuizBot_Engagement',
        KeySchema=[
            {
                'AttributeName': 'quiz_no',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'quiz_no',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_QuizBot_Engagement')
    
if 'UAT_QuizBot_Polls' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_QuizBot_Polls',
        KeySchema=[
            {
                'AttributeName': 'poll_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'poll_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_QuizBot_Polls')
    
if 'UAT_QuizBot_Session' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_QuizBot_Session',
        KeySchema=[
            {
                'AttributeName': 'quiz_no',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'quiz_no',
                'AttributeType': 'N'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_QuizBot_Session')

if 'UAT_StoryBuilding_Bank' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_StoryBuilding_Bank',
        KeySchema=[
            {
                'AttributeName': 'prompt',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'prompt',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_StoryBuilding_Bank')

# ADD INDEX KEY AS DATE IN THIS TABLE
if 'UAT_StoryBuilding_Data' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_StoryBuilding_Data',
        KeySchema=[
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_StoryBuilding_Data')

if 'UAT_Temp_JumbledWord_Session' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_Temp_JumbledWord_Session',
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
    print('create table UAT_Temp_JumbledWord_Session')

if 'UAT_User_Points' not in existing_tables:
    dynamodb.create_table(
        TableName='UAT_User_Points',
        KeySchema=[
            {
                'AttributeName': 'User_id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'User_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    print('create table UAT_User_Points')