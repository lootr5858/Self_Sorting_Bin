import bluetooth
import time

port = 1
bt_address = "98:D3:A1:FD:44:B3"
rpi_bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
rpi_bt.connect((bt_address, port))

while True:
    try:
        send_data = "1"
        rpi_bt.send(send_data.encode('utf-8'))
        print(send_data)
        time.sleep(1)
        
    except KeyboardInterrupt:
        break

rpi_bt.close()
