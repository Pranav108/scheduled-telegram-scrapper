import boto3
import sys,os
from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getcwd())
from config import * 
print('dynamodb connected!!....')

dynamodb = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
    'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
existing_tables = [table.name for table in dynamodb.tables.all()]

if content_analysis not in existing_tables:
    dynamodb.create_table(
        TableName=content_analysis,
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
    print(f"created table {user_master}")
    
if user_master not in existing_tables:
    dynamodb.create_table(
        TableName=user_master,
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
    print(f"created table {user_master}")
    
if user_data not in existing_tables:
    dynamodb.create_table(
        TableName=user_data,
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
    print(f"created table {user_data}")
    
if telegram_master not in existing_tables:
    dynamodb.create_table(
        TableName=telegram_master,
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
    print(f"created table {telegram_master}")

if wcb_data not in existing_tables:
    dynamodb.create_table(
        TableName=wcb_data,
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
    print(f"created table {wcb_data}")
    
if jumbledword_bank not in existing_tables:
    dynamodb.create_table(
        TableName=jumbledword_bank,
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
    print(f"created table {jumbledword_bank}")
    
if jumbledword_engagement not in existing_tables:
    dynamodb.create_table(
        TableName=jumbledword_engagement,
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
    print(f"created table {jumbledword_engagement}")

# ADD INDEX KEY IN THIS TABLE
if quizbot_bank not in existing_tables:
    dynamodb.create_table(
        TableName=quizbot_bank,
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
    print(f"created table {quizbot_bank}")
    
if quizbot_engagement not in existing_tables:
    dynamodb.create_table(
        TableName=quizbot_engagement,
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
    print(f"created table {quizbot_engagement}")
    
if quizbot_polls not in existing_tables:
    dynamodb.create_table(
        TableName=quizbot_polls,
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
    print(f"created table {quizbot_polls}")
    
if quizbot_session not in existing_tables:
    dynamodb.create_table(
        TableName=quizbot_session,
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
    print(f"created table {quizbot_session}")

if storybuilding_bank not in existing_tables:
    dynamodb.create_table(
        TableName=storybuilding_bank,
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
    print(f"created table {storybuilding_bank}")

# ADD INDEX KEY AS DATE IN THIS TABLE
if storybuilding_data not in existing_tables:
    dynamodb.create_table(
        TableName=storybuilding_data,
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
    print(f"created table {storybuilding_data}")

if temp_jumbledword_session not in existing_tables:
    dynamodb.create_table(
        TableName=temp_jumbledword_session,
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
    print(f"created table {temp_jumbledword_session}")

if user_points not in existing_tables:
    dynamodb.create_table(
        TableName=user_points,
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
    print(f"created table {user_points}")