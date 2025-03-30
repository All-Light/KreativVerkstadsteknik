import cv2
import threading
import time
from ServoController import Servo
from CameraController import Camera

class Overwatch:
    """
    Attributes:
        state:
            -1 : Loading
            0 : Searching
            1 : Found/Following target


    """
    def __init__(self, yaw_pin, pitch_pin, camera_index=0, displayFeed=True, boundingBox=0.5, debug=False):
        """
        Initialize the Overwatch controller.

        :param yaw_pin: GPIO pin number for yaw-servo .
        :param pitch_pin: GPIO pin number for pitch-servo .
        :param camera_index: Index of the camera (default: 0 for primary camera).
        :param displayFeed: If the camera feed should be displayed in a window.
        :param boundingBox: Bounding box (part of camera dimensions) where servos will move if the faces is outside of, 0-1.
        """
        self.state = -1
        try:
            self.servoYaw = Servo(pin=yaw_pin, min_angle=-90, max_angle=90, debug=debug)
            self.servoPitch = Servo(pin=pitch_pin, min_angle=0, max_angle=40, debug=debug)
        except IOError as e:
            print(e)

        try: 
            self.camera = Camera(using_rpiCam=True, camera_index=camera_index, debug=debug)
        except IOError as e:
            print(e)

        self.displayFeed = displayFeed
        self.boundingBox = boundingBox
        self.state = 0
        self.debug = debug
        self.running = False
        self.servo_thread = None
        self.camera_thread = None

    def start(self):
        self.running = True
        self.servoYaw.force_angle(0)
        self.servoPitch.force_angle(0)

        # Start threads
        self.servo_thread = threading.Thread(target=self.servo_loop)
        self.camera_thread = threading.Thread(target=self.camera_loop)

        self.servo_thread.start()
        self.camera_thread.start()

    def stop(self):
        self.running = False
        if self.servo_thread:
            self.servo_thread.join()
        if self.camera_thread:
            self.camera_thread.join()

    def servo_loop(self):
        last_yaw_angle = None
        last_pitch_angle = None

        while self.running:
            current_yaw_angle = self.servoYaw.get_internal_angle()
            current_pitch_angle = self.servoPitch.get_internal_angle()

            # Update only if the angle has changed
            if current_yaw_angle != last_yaw_angle: 
                print(f'new yaw: {current_yaw_angle}')
                self.servoYaw.force_angle(current_yaw_angle)
                last_yaw_angle = current_yaw_angle

            if current_pitch_angle != last_pitch_angle:
                print(f'new pitch: {current_pitch_angle}')
                self.servoPitch.force_angle(current_pitch_angle)
                last_pitch_angle = current_pitch_angle

            time.sleep(1)  # Sleep to reduce jittering

    def camera_loop(self):
        try:
            while self.running:
                if self.displayFeed:
                    self.camera.displayCamera()

                if self.camera.see_face():
                        self.state = 1
                else:
                    self.state = 0

                self.execute_state()
                if(cv2.waitKey(1) == ord('q')):
                    break
                time.sleep(0.01)  # Small delay to avoid high CPU usage
        except KeyboardInterrupt:
            self.running = False
            print("\nProgram interrupted by user.")
            
        except Exception as e:
            self.running = False
            print(f"An error occurred: {e}")

        finally:
            self.stop()
            self.servoYaw.cleanup()
            self.servoPitch.cleanup()
            self.camera.cleanup()
            cv2.destroyAllWindows()
    
    def execute_state(self):
        if self.state == 0:
            self.search()
        elif self.state == 1:
            self.follow()

    def search(self):
        '''Implement iterative search'''
        pass

    def follow(self):
        x,y = self.camera.get_face_direction_from_origin()
        if(x == 0 and y == 0): 
            return # no face detected
        if(self.debug):
            print(f"FACE FOUND AT {x},{y}")
        box_width = self.boundingBox* self.camera.width 
        box_height = self.boundingBox * self.camera.height

        left = -box_width / 2
        right = box_width / 2
        top = -box_height / 2
        bottom = box_height / 2
        if x < left:
            if(self.debug):
                print("left")
                print(-62.2*x/(self.camera.width/2))
            self.servoYaw.update_angle(-62.2*x/(self.camera.width), delay=0)

        elif x > right:
            if(self.debug):
                print("right")
                print(-62.2*x/(self.camera.width/2))

            self.servoYaw.update_angle(-62.2*x/(self.camera.width), delay=0)

        if y < top:
            if(self.debug):
                print("above")
                print(48.8*y/(self.camera.height/2))
            self.servoPitch.update_angle(-48.8*y/(self.camera.height), delay=0)

        elif y > bottom:
            if(self.debug):
                print("below")
                print(-48.8*y/(self.camera.height/2))
            self.servoPitch.update_angle(-48.8*y/(self.camera.height), delay=0)
        self.state = 0
