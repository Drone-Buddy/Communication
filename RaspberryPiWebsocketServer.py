import websocket
import json
from datetime import datetime

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    if "gpsdata: " in message:
        gpsdata = message.replace("gpsdata: ", '')
        print("[" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S::%f')[:-3]) + "] ==> Recieved GPS Data: " + gpsdata)
    else:
        print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        while True:
            time.sleep(5)
            send_data = {
                "action": "test",
                "data": "ping",
                "id": "0"
            }
            send = json.dumps(send_data)
            ws.send(send)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    # ws = websocket.WebSocketApp("ws://echo.websocket.org/",
    #                             on_message=on_message,
    #                             on_error=on_error,
    #                             on_close=on_close)
    ws = websocket.WebSocketApp("wss://10eoew3urf.execute-api.us-east-1.amazonaws.com/development",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
