
import RPi.GPIO as GPIO
from ServoController import Servo
from CameraController import Camera
# Example usage
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    try:
        servo1 = Servo(chip=0, pin=17)  # Create servo object for GPIO 17
        servo2 = Servo(chip=0, pin=18)  # Create servo object for GPIO 18

        print("Moving servo 1 to 45 degrees...")
        servo1.set_angle(45)

        print("Incrementing servo 2 by 30 degrees...")
        servo2.update_angle(30)

        print("Moving servo 1 back to 90 degrees with steps...")
        servo1.update_angle(-45, speed=0.05)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        servo1.cleanup()
        servo2.cleanup()
