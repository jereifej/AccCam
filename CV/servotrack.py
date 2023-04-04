from gpiozero import Servo
from time import sleep
import time
from gpiozero.pins.pigpio import PiGPIOFactory
import serial
import struct

# initialize serial port
ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

# initialize the servo pin
factory = PiGPIOFactory()
servo = Servo(25, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000, pin_factory=factory)

# initial position at 90 deg
servo.value=0

# reset serial input
ser.reset_input_buffer()
print("uart connected")

start = time.time()

while True:   
               
        while time.time()-start > 0.005:
            while ser.in_waiting:
                
                # reads the angle
                data_in = struct.unpack('f', ser.read(4))
                angle = data_in[0]
        #         print(angle[0])

                # convert the range of angle(-180, 180) (data_in min, data_in max) into (-1, 1) (servo_value min, servo_value max)
                servo_angle = ((angle+180)/(360))*(2)+(-1)
                servo.value = servo_angle
                print(servo_angle)
                sleep(0.005)
      
      
      
      
#         if (data_in > 187) and (data_in < 97):			# If in the center, good
#              servo.value = 0
#         else:
#         sleep(0.005)
#         angle = ((data_in)/(180))*(2)+(-1)
#         servo.value = angle
#             #set start time
#         print("servo", angle)
#         sleep(0.005)
#         # otherwise keep polling
