import boto3
import json

from botocore.exceptions import ClientError


class DynamoDBAccess:
    dynamo_db = None
    dynamo_db_client = None
    api_client = None
    users_table = None
    drones_table = None

    def add_user(self, database_hash, username, gtid, websocket="None"):
        if websocket is None:
            websocket = "None"
        self.users_table.put_item(
            Item={
                'Id': database_hash,
                'username': username,
                'gtid': gtid,
                'gpsdata': "somewhere on earth",
                'websocket': websocket
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
        response = self.users_table.get_item(
            Key={
                'Id': str(user_id)
            }
        )
        item = response['Item']
        item['gpsdata'] = str(newgpsdata)
        self.users_table.put_item(Item=item)

    def update_user_websocket(self, user_id, websocket):
        response = self.users_table.get_item(
            Key={
                'Id': str(user_id)
            }
        )
        item = response['Item']
        item['websocket'] = str(websocket)
        self.users_table.put_item(Item=item)

    def add_drone(self, websocket="None"):
        if websocket is None:
            websocket = "None"
        count = self.drones_table.scan()['Count']
        self.drones_table.put_item(
            Item={
                'Id': count,
                'gpsdata': "somewhere on earth",
                'websocket': websocket
            }
        )
        return count

    def get_drone_gps(self, drone_id):
        return self.get_drone_entry(drone_id, 'gpsdata')
        
    def get_drone_entry(self, drone_id, entry):
        try:
            response = self.drones_table.get_item(
                Key={
                    'Id': int(drone_id)
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response['Item'][entry]

    def update_drone_gps(self, drone_id, newgpsdata):
        response = self.drones_table.get_item(
            Key={
                'Id': int(drone_id)
            }
        )
        item = response['Item']
        item['gpsdata'] = str(newgpsdata)
        self.drones_table.put_item(Item=item)


    def update_drone_websocket(self, drone_id, websocket):
        response = self.drones_table.get_item(
            Key={
                'Id': int(drone_id)
            }
        )
        item = response['Item']
        item['websocket'] = str(websocket)
        self.drones_table.put_item(Item=item)

    def send_gps_from_user_to_drone(self, send_to_drone_id, gps_data):
        message = f'{"gpsdata"}: {str(gps_data)}'.encode('utf-8')
        response = self.drones_table.get_item(
            Key={
                'Id': int(send_to_drone_id)
            }
        )
        item = response['Item']
        websocket = item.get('websocket')
        if websocket is not None:
            try:
                self.api_client.post_to_connection(Data=message, ConnectionId=websocket)
            except ApiGatewayManagementApi.Client.exceptions.GoneException:
                item['websocket'] = 'None'
                self.users_table.put_item(Item=item)
                return False
            except:
                item['websocket'] = 'None'
                self.users_table.put_item(Item=item)
                return False
            return True


    def get_tables(self):
        return self.dynamo_db_client.list_tables().get('TableNames')

    def __init__(self, is_lambda=False):
        if is_lambda:
            self.dynamo_db = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
            self.dynamo_db_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
            self.api_client = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url="https://10eoew3urf.execute-api.us-east-1.amazonaws.com/development")

        else:
            self.dynamo_db = boto3.resource('dynamodb', region_name='us-east-1', aws_access_key_id="AKIA33UXEMX3DN3F2FWZ", aws_secret_access_key="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")
            self.dynamo_db_client = boto3.client('dynamodb', region_name='us-east-1', aws_access_key_id="AKIA33UXEMX3DN3F2FWZ", aws_secret_access_key="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")
            self.api_client = boto3.client('apigatewaymanagementapi', region_name='us-east-1', aws_access_key_id="AKIA33UXEMX3DN3F2FWZ", aws_secret_access_key="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", endpoint_url="https://10eoew3urf.execute-api.us-east-1.amazonaws.com/development")
        self.drones_table = self.dynamo_db.Table('DronesTable')
        self.users_table = self.dynamo_db.Table('UsersTable')
