import json
import DynamoDBAccess
from OperationHandler import operation_failed, update_websocket_id, add_user_lambda, set_gps, get_gps, ping


def lambda_handler(event, context):
    user_input = event.get('body')

    db = DynamoDBAccess.DynamoDBAccess()

    if user_input is None:
        return operation_failed(event, 'Invalid Message --> No json body found.')

    user_input = json.loads(event.get('body'))

    if user_input.get('data') == 'test':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'Test Complete.',
                'event': event
            })
        }

    if user_input.get('data') == 'ping':
        return ping(event, user_input, db)

    operation = user_input.get('operation')

    update_websocket_id(event, user_input, db)

    if operation == 'add user':
        return add_user_lambda(event, user_input, db)

    if user_input.get('type') is None:
        return operation_failed(event, 'Unable to get your TYPE for setting the gps data')

    if operation == 'set gps':
        return set_gps(event, user_input, db)
    elif operation == 'get gps':
        return get_gps(event, user_input, db)
    else:
        return operation_failed(event, 'NOT a valid operation.')

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
    # print(lambda_handler(
    #     {
    #         "requestContext": {
    #             "routeKey": "test",
    #             "messageId": "U_vNtdtRIAMCIoA=",
    #             "eventType": "MESSAGE",
    #             "extendedRequestId": "U_vNtEwHIAMFoxg=",
    #             "requestTime": "26/Oct/2020:01:52:49 +0000",
    #             "messageDirection": "IN",
    #             "stage": "development",
    #             "connectedAt": 1603677165298,
    #             "requestTimeEpoch": 1603677169209,
    #             "identity": {
    #                 "cognitoIdentityPoolId": "null",
    #                 "cognitoIdentityId": "null",
    #                 "principalOrgId": "null",
    #                 "cognitoAuthenticationType": "null",
    #                 "userArn": "null",
    #                 "userAgent": "null",
    #                 "accountId": "null",
    #                 "caller": "null",
    #                 "sourceIp": "68.50.95.221",
    #                 "accessKey": "null",
    #                 "cognitoAuthenticationProvider": "null",
    #                 "user": "null"
    #             },
    #             "requestId": "U_vNtEwHIAMFoxg=",
    #             "domainName": "10eoew3urf.execute-api.us-east-1.amazonaws.com",
    #             "connectionId": "U_vNFdo2IAMCIoA=",
    #             "apiId": "10eoew3urf"
    #         },
    #         "body": "{\"action\": \"test\", \"operation\": \"get gps\", \"id\": \"0\",\"getid\": \"2\",\"type\": \"drone\",\"gettype\": \"drone\"}",
    #         "isBase64Encoded": "false"
    #     }
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
            "body": "{\"action\": \"test\", \"operation\": \"set gps\", \"id\": \"0\",\"type\": \"drone\",\"gpsdata\": \"test gps data\"}",
            "isBase64Encoded": "false"
        }
        , None))