import bluetooth
import time

port = 1
bt_address = "98:D3:A1:FD:44:B3"
rpi_bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
rpi_bt.connect((bt_address, port))

while True:
    try:
        received_data = rpi_bt.recv(64).decode("utf-8", "ignore")
        print(received_data)

    except KeyboardInterrupt:
        break

rpi_bt.close()
