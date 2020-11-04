import json


def pong(websocket):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'Status': 'pong',
            'websocket': websocket
        })
    }


def operation_completed():
    return {
        'statusCode': 200,
        'body': json.dumps({
            'Status': 'Operation was completed.'
        })
    }


def operation_failed(event, error):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'Status': 'ERROR: Operation was not completed.',
            'reason': str(error),
            'event': event
        })
    }


def ping(event, user_input, db):
    if user_input.get('id') is not None:
        websocket = event.get('requestContext').get('connectionId')
        if websocket is None:
            websocket = "None"
        db.update_drone_websocket(user_input.get('id'), websocket)
        return pong(websocket)
    else:
        return operation_failed(event, 'ID is not valid.')


def add_user_lambda(event, user_input, db):
    database_hash = user_input.get('database_hash')
    username = user_input.get('username')
    gtid = user_input.get('gtid')
    if database_hash is not None and username is not None and gtid is not None:
        db.add_user(database_hash, username, gtid, event.get('requestContext').get('connectionId'))
        return operation_completed()
    else:
        return operation_failed(event, 'Unable to get either your database_hash or username or gtid for adding user')


def update_websocket_id(event, user_input, db):
    websocket = event.get('requestContext').get('connectionId')
    if websocket is None:
        websocket = "None"
    if user_input.get('type') is not None and user_input.get('id') is not None:
        if user_input.get('type') == 'drone':
            db.update_drone_websocket(user_input.get('id'), websocket)
        elif user_input.get('type') == 'user':
            db.update_user_websocket(user_input.get('id'), websocket)


def set_gps(event, user_input, db):
    gps_data = user_input.get('gpsdata')
    type = user_input.get('type')
    if user_input.get('id') is not None:
        id = user_input.get('id')
        if type == 'drone':
            db.update_drone_gps(id, gps_data)
        elif type == 'user':
            db.update_user_gps(id, gps_data)
        else:
            return operation_failed(event, 'Invalid Type.')
        return operation_completed()
    else:
        return operation_failed(event, 'ID is not valid.')


def get_gps(event, user_input, db):
    if user_input.get('getid') is not None and user_input.get('gettype') is not None:
        getid = None
        data = None
        gettype = str(user_input.get('gettype'))
        getid = user_input.get('getid')
        if gettype == 'drone':
            data = db.get_drone_gps(getid)
        elif gettype == 'user':
            data = db.get_user_gps(getid)
        else:
            return operation_failed(event, 'Invalid gettype')
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Status': 'Successfully got gps data.',
                'gpsdata': str(data)
            })
        }

    else:
        return operation_failed(event, 'Unable to get the getid or gettype for setting the gps data')
