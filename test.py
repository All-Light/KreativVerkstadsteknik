import time
import cv2
import numpy as np
from picamera2 import Picamera2

height =480
width=640
middle =((width//2),(height//2))

cam = Picamera2()


cam.configure(cam.create_video_configuration(main={"format": 'XRGB8888', "size": (width, height)}))

cam.start()

print("Press 'q' to quit.")
while True:
    # Capture a frame from the camera
    frame = cam.capture_array()

    # Check if the frame was captured successfully
    if frame is None:
        print("Error: Failed to capture frame.")
        break
    print(f"Captured frame with shape: {frame.shape} and dtype: {frame.dtype}")

    # Convert the frame to BGR format for OpenCV display (Picamera2 uses XRGB8888 by default)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Display the frame using OpenCV
    cv2.imshow("Camera", frame_bgr)

    key = cv2.waitKey(10) & 0xFF
    if key == ord('q'):
        break
    # Break the loop if 'q' is pressed
    #if(cv2.waitKey(1) == ord('q')):
    #    break
cv2.destroyAllWindows()
