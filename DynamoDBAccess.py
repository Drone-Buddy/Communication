import boto3
import json

from botocore.exceptions import ClientError


class DynamoDBAccess:
    dynamo_db = None
    dynamo_db_client = None
    users_table = None
    drones_table = None

    def add_user(self, database_hash, username, gtid):
        self.users_table.put_item(
            Item={
                'Id': database_hash,
                'username': username,
                'gtid': gtid,
                'gpsdata': "somewhere on earth"
            }
        )

    def get_user_gps(self, user_id):
        try:
            response = self.users_table.get_item(
                Key={
                    'Id': str(user_id)
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']['gpsdata']

    def update_user_gps(self, user_id, newgpsdata):
        self.users_table.update_item(
            Key={
                'Id': str(user_id)
            },
            UpdateExpression="set gpsdata=:g",
            ExpressionAttributeValues={
                ':g': str(newgpsdata)
            },
            ReturnValues="UPDATED_NEW"
        )

    def add_drone(self):
        count = self.drones_table.scan()['Count']
        self.drones_table.put_item(
            Item={
                'Id': count,
                'gpsdata': "somewhere on earth"
            }
        )
        return count

    def get_drone_gps(self, drone_id):
        try:
            response = self.drones_table.get_item(
                Key={
                    'Id': int(drone_id)
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item']['gpsdata']

    def update_drone_gps(self, drone_id, newgpsdata):
        self.drones_table.update_item(
            Key={
                'Id': int(drone_id)
            },
            UpdateExpression="set gpsdata=:g",
            ExpressionAttributeValues={
                ':g': str(newgpsdata)
            },
            ReturnValues="UPDATED_NEW"
        )

    def get_tables(self):
        return self.dynamo_db_client.list_tables().get('TableNames')

    def __init__(self, is_lambda=False):
        if is_lambda:
            self.dynamo_db = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
            self.dynamo_db_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
        else:
            self.dynamo_db = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id="AKIA33UXEMX3DN3F2FWZ", aws_secret_access_key="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")
            self.dynamo_db_client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id="AKIA33UXEMX3DN3F2FWZ", aws_secret_access_key="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")
        self.drones_table = self.dynamo_db.Table('DronesTable')
        self.users_table = self.dynamo_db.Table('UsersTable')
