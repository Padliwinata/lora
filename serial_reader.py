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
    timeout = time.time() + sec
    file = open('data.txt', 'a')
    while True:
        if time.time() > timeout:
            break
        value = ser.readline().decode('UTF-8')
        value.rstrip()
        file.write(value)
    file.close()


def send_data(sec: int):
    timeout = time.time() + sec
    while True:
        file = open('data.txt', 'a')
        if time.time() > timeout:
            break
        value = ser.readline().decode('UTF-8')
        value.rstrip()
        file.write(value)
    file.close()
    while True:
        datas = []
        with open('data.txt', 'r') as file:
            for line in file:
                if line:
                    if line[0].isdigit():
                        line = line.replace("WAIT...", "")
                        res = regex.findall(line)
                        now = datetime.datetime.now()
                        if len(res) != 0:
                            data = {
                                'params': 'insert-data',
                                'records': {
                                    'date': now.strftime("%Y-%m-%d"),
                                    'time': now.strftime("%H:%M"),
                                    'voltage': res[0][4],
                                    'current': res[0][3],
                                    'battery': res[0][2]
                                },
                                'device': res[0][1]
                            }
                            # datas.append()
                            print(data)

        # response = requests.post('http://tomas.pgn-solution.co.id:14000/api/public/device/smart-tb', json=data)
        # if response.status_code == 200:
        # print(data)
        os.remove('data.txt')
        print()


if __name__ == "__main__":
    while True:
        send_data(10)
