import re

import serial
from serial.serialutil import SerialException

regex = re.compile(r"((\d) VD(\d+\.\d)\s+A-(\d+\.\d)\s+B(\d+\.\d))")
ser = None
try:
    ser = serial.Serial('/dev/ttyUSB0')
    ser.flushInput()
except SerialException as e:
    print(e)

with open('dataFile.txt', 'a') as file:
    while True:
        try:
            value = ser.readline().decode('UTF-8')
            file.write(value)
            print(value)
            # ser_bytes = ser.readline()
            # decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode('latin-1'))
            # print(decoded_bytes)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break
