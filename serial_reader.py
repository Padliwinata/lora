import re
import time
import os
import requests
import datetime

import serial
from serial.serialutil import SerialException

regex = re.compile(r"((\d) VD(\d+\.\d)\s+A-(\d+\.\d)\s+B(\d+\.\d))")
ser = None
try:
    ser = serial.Serial('/dev/ttyUSB0')
    ser.flushInput()
except SerialException as e:
    print(e)


def write_data(sec: int):
    while True:
        timeout = time.time() + sec
        file = open('data.txt', 'a')
        while True:
            if time.time() > timeout:
                break
            value = ser.readline().decode('UTF-8')
            value.rstrip()
            file.write(value)
        file.close()
        with open('data.txt', 'r') as file:
            for line in file:
                if line[0].isdigit():
                    line = line.replace("WAIT...", "")
                    res = regex.findall(line)
                    now = datetime.datetime.now()
                    records = [
                        {
                            'date': now.strftime("%Y-%m-%d"),
                            'time': now.strftime("%H:%M"),
                            'voltage': res[0][4],
                            'current': res[0][3],
                            'battery': res[0][2]
                        }
                    ]
                    requests.post('http://tomas.pgn-solution.co.id:14000/device/smart-tb', json={
                        'params': 'insert-data',
                        'records': records,
                        'device': res[0][1]
                    })
                    print(records)
                    print("end")
        os.remove('data.txt')
        print("end")


if __name__ == "__main__":
    write_data(10)
