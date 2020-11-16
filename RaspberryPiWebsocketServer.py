#!/usr/bin/python3
import websocket
import json
import serial
from datetime import datetime
import _thread as thread
import time
import threading


class GPSStream:
    """Manage the serial connection."""

    def __init__(self, port, data):
        self.port = serial.Serial(port=port, 
                                  baudrate=9600,
                                  bytesize=serial.EIGHTBITS,
                                  parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE)
        self.data = data
        self.keep_alive()


    def send(self, data):
        """
        Update the message that we're sending.
        """
        self.data = data


    def tick(self):
        """
        Update the message's timestamp and construct the sentence.
        """
        self.data['timestamp'] = datetime.now().timestamp()*1000
        self.msg = construct_gpgga(self.data)


    def keep_alive(self):
        """
        Keep the connection alive with
        valid data.
        """
        self.tick()
        self.port.write(self.msg)
        threading.Timer(0.5, self.keep_alive).start()
        print(f'Sent: {self.msg}')


def construct_gpgga(data):
    """Construct an NMEA GPGGA sentence from raw data"""
    fix = data.get('fix', 1)

    if fix:
        utc = ms_to_utc(int(data['timestamp']))
        lat = float(data['latitude'])
        long = float(data['longitude'])
        num_sats = 15
        hdop = 1.5
        altitude = float(data['altitude'])
        dsep_geoid = 0
        dgps_delta_t = ''
        dgps_station = ''

        if lat < 0:
            lat_hemi = 'S'
            lat = -lat
        else:
            lat_hemi = 'N'

        if long < 0:
            long_hemi = 'W'
            long = -long
        else:
            long_hemi = 'E'

        lat_degdmin = f'{int(lat):0>2d}{cvt_deg_to_dmin(lat-int(lat)):.4f}'
        long_degdmin = f'{int(long):0>3d}{cvt_deg_to_dmin(long-int(long)):.4f}'

        sentence = f'GPGGA,{utc},{lat_degdmin},{lat_hemi},{long_degdmin},{long_hemi},{fix},{num_sats},{hdop:.1f},{altitude:.1f},M,{dsep_geoid:.1f},M,{dgps_delta_t},{dgps_station}'
    else:
        utc = ''
        lat = ''
        lat_hemi = ''
        long = ''
        long_hemi = ''
        num_sats = '00'
        hdop = '99.99'
        altitude = ''
        dsep_geoid = ''
        dgps_delta_t = ''
        dgps_station = ''
        sentence = f'GPGGA,{utc},{lat},{lat_hemi},{long},{long_hemi},{fix},{num_sats},{hdop},{altitude},,{dsep_geoid},,{dgps_delta_t},{dgps_station}'

    checksum = compute_checksum(sentence)
    return f'${sentence}*{checksum:X}\r\n'.encode(encoding='utf-8', errors='strict')


def compute_checksum(sentence):
    """Compute checksum of NMEA sentence"""
    s = 0
    for c in sentence:
        s = s ^ ord(c)

    return s


def ms_to_utc(ms):
    """Convert POSIX timestamp to UTC time string"""
    return datetime.utcfromtimestamp(ms/1000.0).strftime('%H%M%S.%f')[:-3]
    

def cvt_deg_to_dmin(deg):
    """Convert decimal degrees to decimal minutes"""
    return deg * 60


def on_message(ws, message, gps_stream):
    if "gpsdata: " in message:
        data = json.loads(message.lstrip("gpsdata: ").replace("\'", "\""))
        gps_stream.send(data)


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
    mock_data = { 'fix': 0 }
    gps_stream = GPSStream(port='/dev/serial0', data=mock_data)
    print('Sending GPS data to serial port: ' + gps_stream.port.name) 
    
    # For Debug:
    # websocket.enableTrace(True)
    print('Starting WebSocket connection to AWS.')
    ws = websocket.WebSocketApp("wss://10eoew3urf.execute-api.us-east-1.amazonaws.com/development",
                                on_message=lambda ws, msg: on_message(ws, msg, gps_stream),
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
