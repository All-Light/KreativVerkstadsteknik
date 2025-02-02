from OverwatchController import Overwatch
from ServoController import Servo
from CameraController import Camera

import time

if __name__ == "__main__":
    overwatch = Overwatch(yaw_pin=19, pitch_pin=18, camera_index=0, displayFeed=False, boundingBox=0.3)
    overwatch.start()
