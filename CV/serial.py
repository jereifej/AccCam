# import time
# import serial
#
# ser = serial.Serial('COM16', 115200, timeout=1)
# count = 0
#
# while 1:
#     while ser.in_waiting:
#         data_in = ser.readline()
#         print(data_in)

import time
import serial

ser = serial.Serial('COM16', 115200, timeout=1)
count = 0

while True:
    ser.write(b'hello\n')
    time.sleep(0.05)
    count += 1
    print('sent')


#    ser.write('Sent %d time(s)')
#    time.sleep(1)
#    count += 1