import serial
from serial.serialutil import SerialException


ser = None
try:
    ser = serial.Serial('/dev/ttyUSB0')
    ser.flushInput()
except SerialException as e:
    print(e)

while True:
    try:
        ser_bytes = ser.readline()
        decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode('utf-8'))
        print(decoded_bytes)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
        break
