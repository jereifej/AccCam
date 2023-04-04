from gpiozero import AngularServo
from time import sleep
import time
from gpiozero.pins.pigpio import PiGPIOFactory
import serial
import struct

# initialize serial port
ser = serial.Serial("/dev/ttyAMA0", 115200, timeout=1)

# initialize the servo pin
factory = PiGPIOFactory()
servo = AngularServo(25, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000, pin_factory=factory)

# initial position at 90 deg
# servo.angle= 90
# sleep(0.5)
# servo.angle= 10
# sleep(0.5)
# servo.angle= -90
# sleep(0.5)
servo.angle= 10
# reset serial input
ser.reset_input_buffer()
print("uart connected")

start = time.time()

while True:
    while time.time()-start > 0.05:
        while ser.in_waiting:
            
            # reads the angle
            data_in = struct.unpack('f', ser.read(4))
            angle = data_in[0]
    #         print(angle[0])
            print("angle", angle)
            
            if angle < -5:
            
                # convert the range of angle(-180, 180) (data_in min, data_in max) to (-1, 1) (servo_value min, servo_value max)
                #servo_angle = ((angle-180)/(-360))*(2)+(-1)
                servo.angle -= 1.5
                print("servo", angle)
                sleep(0.005)
            
            elif angle > 5:
                servo.angle += 1.5
                print("servo", angle)
                sleep(0.005)
      
      
