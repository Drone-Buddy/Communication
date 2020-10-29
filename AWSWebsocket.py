import unittest
import json
import asyncio
import websocket

GREEN = '\033[92m'
RESET = '\033[0m'

aws_websocket_url = 'wss://10eoew3urf.execute-api.us-east-1.amazonaws.com/development'


def send_websocket(data):
    websocket_object = websocket.create_connection(aws_websocket_url)
    websocket_object.send(data)
    result = websocket_object.recv()
    result = json.loads(result)
    websocket_object.close()
    return result


class TestWebsocket(unittest.TestCase):

    def StartWebsocket(self):
        websocket_object = websocket.create_connection(aws_websocket_url)
        # print(websocket_object)
        self.assertEqual(websocket_object.getstatus(), 101)
        websocket_object.send("{\"action\": \"test\", \"data\": \"test\"}")
        # print(GREEN + '### Sent Test to WebSocket' + RESET)
        result = websocket_object.recv()
        # print(GREEN + '### Recv Test to WebSocket ==> ' + result + RESET)
        result = json.loads(result)
        self.assertEqual(result.get('Status'), "Test Complete.")


class TestGps(unittest.TestCase):

    test_gps_data = "Indiana, USA"

    def InvalidTest(self):
        result = send_websocket("{\"action\": \"test\", \"data\": \"invalid\"}")
        self.assertEqual(result.get('Status'), "ERROR: Operation was not completed.")
        self.assertEqual(result.get('reason'), "Unable to get your ID or TYPE for setting the gps data")

    def InvalidOperation(self):
        send_data_op = {
            "action": "test",
            "operation": "invalid",
            "id": 0,
            "type": "drone"
        }
        send_data = json.dumps(send_data_op)
        result = send_websocket(send_data)
        self.assertEqual(result.get('Status'), "ERROR: Operation was not completed.")
        self.assertEqual(result.get('reason'), "NOT a valid operation.")

    def SetGpsData(self):
        send_data_op = {
            "action": "test",
            "operation": "set gps",
            "id": 2,
            "gpsdata": str(self.test_gps_data),
            "type": "drone"
        }
        send_data = json.dumps(send_data_op)
        result = send_websocket(send_data)
        self.assertEqual(result.get('Status'), "Operation was completed.")

    def GetGpsData(self):
        send_data_op = {
            "action": "test",
            "operation": "get gps",
            "id": "0",
            "getid": "2",
            "type": "drone",
            "gettype": "drone"
        }
        send_data = json.dumps(send_data_op)
        result = send_websocket(send_data)
        self.assertEqual(result.get('Status'), "Successfully got gps data.")
        self.assertEqual(result.get('gpsdata'), str(self.test_gps_data))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestWebsocket('StartWebsocket'))
    suite.addTest(TestGps('InvalidTest'))
    suite.addTest(TestGps('InvalidOperation'))
    suite.addTest(TestGps('SetGpsData'))
    suite.addTest(TestGps('GetGpsData'))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
