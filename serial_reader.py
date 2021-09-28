import datetime
import json
import os
import re
import requests
from requests import ConnectionError
import time

import serial
from serial.serialutil import SerialException


regex = re.compile(r"((\d)\sV(\d+\.\d)\s+A(\d+\.\d)\s+B(\d+\.\d))")

while True:
    try:
        ser = serial.Serial('COM5')
        ser.flushInput()
        break
    except SerialException as e:
        print(e)
        continue


def read_and_send(sec: int):
    while True:
        timeout = time.time() + sec
        file = open('gateway_data.txt', 'a')
        while True:
            if time.time() > timeout:
                break
            value = ser.readline().decode('utf-8')
            file.write(value)
        file.close()
        with open('gateway_data.txt', 'r') as file:
            for line in file:
                if line[0].isdigit():
                    line = line.rstrip()
                    res = regex.findall(line)
                    if len(res) != 0:
                        print(f"Device: \t{res[0][1]}")
                        print(f"Voltase:\t{res[0][2]}")
                        print(f"Arus:\t\t{res[0][3]}")
                        print(f"Baterai:\t{res[0][4]}")
                        print()
                        data = {
                            'params': 'insert-data',
                            'records': [
                                {
                                    'date': datetime.datetime.now().strftime("%Y-%m-%d"),
                                    'time': datetime.datetime.now().strftime("%H:%M"),
                                    'voltage': res[0][2],
                                    'current': res[0][3],
                                    'battery': round(float(res[0][4]), 0)
                                }
                            ],
                            'device': str(res[0][1])
                        }

                        res = requests.post('http://tomas.pgn-solution.co.id:14000/api/public/device/smart-tb', json=data)
        os.remove('gateway_data.txt')
        print(res.content)


if __name__ == '__main__':
    read_and_send(30)


