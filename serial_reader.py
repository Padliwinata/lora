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
        records = []
        with open('data.txt', 'r') as file:
            for line in file:
                if line:
                    if line[0].isdigit():
                        line = line.replace("WAIT...", "")
                        res = regex.findall(line)
                        now = datetime.datetime.now()
                        records.append({
                            'date': now.strftime("%Y-%m-%d"),
                            'time': now.strftime("%H:%M"),
                            'voltage': res[0][4],
                            'current': res[0][3],
                            'battery': res[0][2]
                        })
                        print("end")
        # data = {
        #     'params': 'insert-data',
        #     'records': records,
        #     'device': res[0][1]
        # }
        # response = requests.post('http://tomas.pgn-solution.co.id:14000/api/public/device/smart-tb', json=data)
        # if response.status_code == 200:
        print(records)
        os.remove('data.txt')
        # print("end")


if __name__ == "__main__":
    write_data(10)
