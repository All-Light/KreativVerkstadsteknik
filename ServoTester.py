from gpiozero import Servo
from time import sleep

servo1 = Servo(18)  
servo2 = Servo(19)
# Move the servo
try:
    while True:
        print("Max position")
        servo1.max()
        servo2.max()
        sleep(1)
        print("Mid position")
        servo1.mid()
        servo2.mid()
        sleep(1)
        print("Min position")
        servo1.min()
        servo2.min()
        sleep(1)
except KeyboardInterrupt:
    print("Exiting...")