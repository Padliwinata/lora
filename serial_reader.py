import re
import time

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
            file.write(value)
        file.close()
        print("write")


if __name__ == "__main__":
    write_data(30)
