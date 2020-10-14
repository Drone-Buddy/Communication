import json


def lambda_handler(event, context):

    user_input = event.get('body')

    if user_input is None:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'Invalid Message --> No json body found.'
            })
        }

    user_input = json.loads(event.get('body'))

    operation = user_input.get('operation')

    if user_input.get('id') is None:
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'ERROR: Operation was not completed.',
                'reason': 'Unable to get your ID for setting the gps data'
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
            'Hello': 'Hello from Lambda!',
            'connectionId': event['requestContext']['connectionId'],
            'event': event
        })
    }

if __name__ == "__main__":
    lambda_handler(json.dumps({
        'Hello': 'Hello from Lambda!',
        'connectionId': 'UYUs-cLQoAMCLEg=',
        'event': {
            'requestContext': {
                'routeKey': 'test',
                'messageId': 'UYUuZcUUIAMCLEg=',
                'eventType': 'MESSAGE',
                'extendedRequestId': 'UYUuZHpuoAMF-Hg=',
                'requestTime': '14/Oct/2020:02:52:37 +0000',
                'messageDirection': 'IN',
                'stage': 'development',
                'connectedAt': 1602643948538,
                'requestTimeEpoch': 1602643957689,
                'identity': {
                    'cognitoIdentityPoolId': 'null',
                    'cognitoIdentityId': 'null',
                    'principalOrgId': 'null',
                    'cognitoAuthenticationType': 'null',
                    'userArn': 'null',
                    'userAgent': 'null',
                    'accountId': 'null',
                    'caller': 'null',
                    'sourceIp': '68.50.95.221',
                    'accessKey': 'null',
                    'cognitoAuthenticationProvider': 'null',
                    'user': 'null'
                },
                'requestId': 'UYUuZHpuoAMF-Hg=',
                'domainName': '10eoew3urf.execute-api.us-east-1.amazonaws.com',
                'connectionId': 'UYUs-cLQoAMCLEg=',
                'apiId': '10eoew3urf'
            },
            'body': '{\'action\':\'test\', \'data\': \'hello\'}',
            'isBase64Encoded': 'false'
        }
    }), None)