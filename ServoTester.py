from gpiozero import AngularServo
from time import sleep

servo1 = AngularServo(18)  
servo2 = AngularServo(19)
# Move the servo
try:
    while True:
        print("Max position")
        servo1.angle = 40
        servo2.angle = 90
        sleep(1)
       	print("Mid position")
        servo1.angle = 0
        servo2.angle = 0
        sleep(1)
        print("Min position")
        servo1.angle = -40
        servo2.angle = -90
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
