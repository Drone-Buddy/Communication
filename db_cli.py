import argparse
import DynamoDBAccess

def cli():
    parser = argparse.ArgumentParser(description='Access AWS Dynamo Database')
    parser.add_argument('-g', dest='gettables', help='Only to get all the Dynamo DB Tables', action='store_true', default=False)
    parser.add_argument('-t', dest='type', choices= ['drone', 'user'] ,help='[\'drone\', \'user\']')
    parser.add_argument('-o', dest='operation', choices=['setgps', 'getgps', 'adddrone'], help='[\'setgps\', \'getgps\', \'adddrone\']') # 'adduser'
    parser.add_argument('-l', dest='gps', help='Place GPS to set for operation=setgps')
    parser.add_argument('-i', dest='id', help='Place ID to set for operation=getgps & setgps')
    args = parser.parse_args()

    db = DynamoDBAccess.DynamoDBAccess()

    if args.gettables:
        print(db.get_tables())
        return

    if args.operation == 'setgps':
        if args.gps is None or args.id is None or args.type is None:
            print('Specify a GPS value with the option\'-l\'')
            return
        if args.type == 'drone':
            db.update_drone_gps(args.id, args.gps)
            print('Done.')
            return
        elif args.type == 'user':
            db.update_user_gps(args.id, args.gps)
            print('Done.')
            return

    if args.operation == 'getgps':
        if args.id is None or args.type is None:
            print('Specify a GPS value with the option\'-l\'')
            return
        gps_val = None
        if args.type == 'drone':
            gps_val = db.get_drone_gps(args.id)
            print('Here is the GPS Data for Drone #' + str(args.id) + ' ==> ' + str(gps_val))
            return
        elif args.type == 'user':
            gps_val = db.get_user_gps(args.id)
            print('Here is the GPS Data for User #' + str(args.id) + ' ==> ' + str(gps_val))
            return

    if args.operation == 'adddrone':
        id = db.add_drone()
        print('New Drone Created with ID: ' + str(id))

if __name__ == "__main__":
    cli()