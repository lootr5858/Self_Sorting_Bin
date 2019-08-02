""" required libraries """
import serial
import RPi.GPIO as GPIO
import time

""" setup your serial comms for GPIO """
comms = serial.Serial('/dev/ttyAMA0', 9600, timeout = 1)
comms.baudrate
comms.close()
comms.open()

""" Write commands to arduino """
while True:
    comms.write(str.encode("0"))
    print("0")
    response = comms.readline()
    print(response)
    time.sleep(1)

    comms.write(str.encode("1"))
    response = comms.readline()
    print(response)
    time.sleep(1)

comms.close()
