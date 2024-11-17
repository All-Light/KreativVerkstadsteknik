from OverwatchController import Overwatch
from ServoController import Servo
from CameraController import Camera

import time

if __name__ == "__main__":
    overwatch = Overwatch(yaw_pin=23, pitch_pin=24, camera_index=0)
    overwatch.start()
