""" include all required libraries & dependancies """
import bluetooth
import time

""" establish bluetooth connection with target """
rpi_bt_port = 1 # RPI's bluetooth port
bt_address = "98:D3:A1:FD:44:B3"    # MAC address of target
rpi_bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
rpi_bt.connect((bt_address, rpi_bt_port))

count = 0
received = ""

""" establish communication with target """
while True:
    time.sleep(2)
    try:
        ''' send instructions to target '''
        rpi_bt.send(str(count % 2))
        print("Send: {}".format(count))
        count += 1
        print("Current count: {}".format(count))

        ''' wait for reply '''
        while received == "":
            received = rpi_bt.recv(10).decode('utf-8', 'ignore')

    except KeyboarInterrupt:
        rpi_bt.close()
        break
