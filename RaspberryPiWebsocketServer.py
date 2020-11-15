import websocket
import json
import serial
from datetime import datetime

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    global serial_comm
    if "gpsdata: " in message:
        gpsdata = message.replace("gpsdata: ", '').replace("\'", "\"")
        gpsdatajson = json.loads(gpsdata)
        nmea = gpsdatajson.get('nmea')
        if nmea is not None:
            if serial_comm is None or serial_comm.is_open is False:
                serial_comm = serial.Serial('/dev/serial0')
            serial_comm.write(nmea.encode())
        print("[" + str(datetime.now().strftime('%Y-%m-%d %H:%M:%S::%f')[:-3]) + "] ==> Recieved GPS NMEA Data: " +
              nmea)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### AWS WebSocket is closed ###")


def on_open(ws):
    def run(*args):
        while True:
            send_data = {
                "action": "test",
                "data": "ping",
                "id": "0"
            }
            send = json.dumps(send_data)
            ws.send(send)
            time.sleep(1)
        ws.close()
        print("Stopping WebSocket Open Thread.")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    global serial_comm
    serial_comm = serial.Serial('/dev/serial0')
    print('Sending gps data to serial port: ' + str(serial_comm.name))
    # For Debug:
    # websocket.enableTrace(True)
    print('Starting WebSocket connection to AWS.')
    ws = websocket.WebSocketApp("wss://10eoew3urf.execute-api.us-east-1.amazonaws.com/development",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
