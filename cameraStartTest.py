from picamera2 import Picamera2

# Initialize Picamera2
cam = Picamera2()

# Try configuring and starting the camera
try:
    cam.start()
    print("Camera initialized successfully!")
except Exception as e:
    print(f"Error initializing camera: {e}")
