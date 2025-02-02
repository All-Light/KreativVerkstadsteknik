from OverwatchController import Overwatch

if __name__ == "__main__":
    overwatch = Overwatch(yaw_pin=19, pitch_pin=18, camera_index=0, displayFeed=False, boundingBox=0.3, debug=False)
    overwatch.start()
