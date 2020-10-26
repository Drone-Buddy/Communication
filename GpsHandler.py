import json


def lambda_handler(event, context):
    user_input = event.get('body')

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

    if user_input.get('id') is None:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'Unable to get your ID for setting the gps data',
                'event': event
            })
        }

    id = user_input.get('id')

    if operation == 'set gps':
        gps_data = user_input.get('gpsdata')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'Operation was completed.'
            })
        }
    elif operation == 'get gps':
        if user_input.get('getid') is not None:
            getid = user_input.get('getid')
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'Status': 'Successfully got gps data.',
                    'gpsdata': 'EARTH'
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
    print(lambda_handler(
    {
        "Hello": "Hello from Lambda!",
        "connectionId": "U_vNFdo2IAMCIoA=",
        "event": {
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
            "body": "{action: \"test\", data: \"test\"}",
            "isBase64Encoded": "false"
        }
    }
        , None))