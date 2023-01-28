import boto3
import os
from dotenv import load_dotenv
load_dotenv()  # this is for the env file loading
class DynamoDB_con():
    def __init__(self):
        self.dynamo_client = boto3.resource(service_name=os.getenv('service_name'), region_name=os.getenv(
            'region_name'), aws_access_key_id=os.getenv('aws_access_key_id'), aws_secret_access_key=os.getenv('aws_secret_access_key'))
    def send_data(self, data, tableName):
        print(data)
        db = self.dynamo_client.Table(tableName)
        db.put_item(Item=data)
        print('Data is sending to the database!!!!')
    def read_read(self, tableName):
        table = self.dynamo_client.Table(tableName)
        response = table.scan()
        data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
        return data, len(data)
    def deleteTotalData(self,table_name='TB_Temp_JumbledWord_Session'):
        flag = False
        table = self.dynamo_client.Table(table_name)
        scan = table.scan()
        while not flag:
            with table.batch_writer() as batch:
                for each in scan['Items']:
                    batch.delete_item(
                                Key={
                                'Id': each['Id']
                                }
                            )
                flag = True