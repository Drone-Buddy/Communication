import json
import DynamoDBAccess

def lambda_handler(event, context):

    user_input = event.get('body')

    db = DynamoDBAccess.DynamoDBAccess()

    if user_input is None:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'Invalid Message --> No json body found.',
                'event': event
            })
        }

    user_input = json.loads(event.get('body'))

    if user_input.get('data') == 'test':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'Test Complete.',
                'event': event
            })
        }

    operation = user_input.get('operation')

    if user_input.get('id') is None or user_input.get('type') is None:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'Unable to get your ID or TYPE for setting the gps data',
                'event': event
            })
        }

    type = user_input.get('type')
    id = user_input.get('id')

    if operation == 'set gps':
        gps_data = user_input.get('gpsdata')
        if type == 'drone':
            db.update_drone_gps(id, gps_data)
        elif type == 'user':
            db.update_user_gps(id, gps_data)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'Operation was completed.'
            })
        }
    elif operation == 'get gps':
        if user_input.get('getid') is not None and user_input.get('gettype') is not None:
            getid = None
            data = None
            gettype = str(user_input.get('gettype'))
            if gettype == 'drone':
                getid = int(user_input.get('getid'))
                data = db.get_drone_gps(getid)
            elif gettype == 'user':
                getid = str(user_input.get('getid'))
                data = db.get_user_gps(getid)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'Status': 'Successfully got gps data.',
                    'gpsdata': data
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'Status': 'ERROR: Operation was not completed.',
                    'reason': 'Unable to get the set ID for setting the gps data'
                })
            }
    else:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'NOT a valid operation.'
            })
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'ERROR': 'This should have been unreachable...',
            'connectionId': event['requestContext']['connectionId'],
            'event': event
        })
    }

if __name__ == "__main__":
    # print(lambda_handler(
    # {
    #     "requestContext": {
    #         "routeKey": "test",
    #         "messageId": "U_vNtdtRIAMCIoA=",
    #         "eventType": "MESSAGE",
    #         "extendedRequestId": "U_vNtEwHIAMFoxg=",
    #         "requestTime": "26/Oct/2020:01:52:49 +0000",
    #         "messageDirection": "IN",
    #         "stage": "development",
    #         "connectedAt": 1603677165298,
    #         "requestTimeEpoch": 1603677169209,
    #         "identity": {
    #             "cognitoIdentityPoolId": "null",
    #             "cognitoIdentityId": "null",
    #             "principalOrgId": "null",
    #             "cognitoAuthenticationType": "null",
    #             "userArn": "null",
    #             "userAgent": "null",
    #             "accountId": "null",
    #             "caller": "null",
    #             "sourceIp": "68.50.95.221",
    #             "accessKey": "null",
    #             "cognitoAuthenticationProvider": "null",
    #             "user": "null"
    #         },
    #         "requestId": "U_vNtEwHIAMFoxg=",
    #         "domainName": "10eoew3urf.execute-api.us-east-1.amazonaws.com",
    #         "connectionId": "U_vNFdo2IAMCIoA=",
    #         "apiId": "10eoew3urf"
    #     },
    #     "body": "{\"action\": \"test\", \"data\": \"test\"}",
    #     "isBase64Encoded": "false"
    # }
    #     , None))
    print(lambda_handler(
    {
        "requestContext": {
            "routeKey": "test",
            "messageId": "U_vNtdtRIAMCIoA=",
            "eventType": "MESSAGE",
            "extendedRequestId": "U_vNtEwHIAMFoxg=",
            "requestTime": "26/Oct/2020:01:52:49 +0000",
            "messageDirection": "IN",
            "stage": "development",
            "connectedAt": 1603677165298,
            "requestTimeEpoch": 1603677169209,
            "identity": {
                "cognitoIdentityPoolId": "null",
                "cognitoIdentityId": "null",
                "principalOrgId": "null",
                "cognitoAuthenticationType": "null",
                "userArn": "null",
                "userAgent": "null",
                "accountId": "null",
                "caller": "null",
                "sourceIp": "68.50.95.221",
                "accessKey": "null",
                "cognitoAuthenticationProvider": "null",
                "user": "null"
            },
            "requestId": "U_vNtEwHIAMFoxg=",
            "domainName": "10eoew3urf.execute-api.us-east-1.amazonaws.com",
            "connectionId": "U_vNFdo2IAMCIoA=",
            "apiId": "10eoew3urf"
        },
        "body": "{\"action\": \"test\", \"operation\": \"get gps\", \"id\": \"0\",\"getid\": \"2\",\"type\": \"drone\",\"gettype\": \"drone\"}",
        "isBase64Encoded": "false"
    }
        , None))