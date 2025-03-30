from OverwatchController import Overwatch

if __name__ == "__main__":
    overwatch = Overwatch(yaw_pin=19, pitch_pin=18, camera_index=0, displayFeed=True, boundingBox=0, debug=True)
    overwatch.start()
