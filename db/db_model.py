import boto3
from boto3.dynamodb.conditions import Key
# from boto3.dynamodb.conditions import KeyConditionExpression,ExpressionAttributeValues
import sys,os
import datetime
from dotenv import load_dotenv
load_dotenv()  # this is for the env file loading
sys.path.append(os.getcwd())
storybuilding_data=os.getenv('storybuilding_data')
quizbot_engagement=os.getenv('quizbot_engagement')
quizbot_session=os.getenv('quizbot_session')

class DynamoDB_con():
    def __init__(self):
        self.dynamo_client = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
            'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
    def send_data(self, data, tableName):
        db = self.dynamo_client.Table(tableName)
        db.put_item(Item=data)
    def read_all_data(self, tableName):
        table = self.dynamo_client.Table(tableName)
        response=table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    def read_data(self, tableName,keyValue,queryValue):
        table = self.dynamo_client.Table(tableName)
        if tableName==storybuilding_data or tableName==quizbot_engagement or tableName==quizbot_session:
            response=table.query(IndexName='date-index',KeyConditionExpression=Key(keyValue).eq(queryValue))
        else:
            response=table.query(KeyConditionExpression=Key(keyValue).eq(queryValue))
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data
    
    def deleteTotalData(self,table_name):
        flag = False
        table = self.dynamo_client.Table(table_name)
        scan = table.scan()
        while not flag:
            with table.batch_writer() as batch:
                for userObj in scan['Items']:
                    batch.delete_item(Key={'User_ID': userObj['User_ID']})
                flag = True