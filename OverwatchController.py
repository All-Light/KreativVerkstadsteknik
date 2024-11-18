import cv2
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
    def __init__(self, yaw_pin, pitch_pin, camera_index=0, displayFeed=True, boundingBox=0.5):
        """
        Initialize the Overwatch controller.

        :param yaw_pin: GPIO pin number for yaw-servo .
        :param pitch_pin: GPIO pin number for pitch-servo .
        :param camera_index: Index of the camera (default: 0 for primary camera).
        :param displayFeed: If the camera feed should be displayed in a window.
        :param boundingBox: Bounding box (part of camera dimensions) where servos will move if the faces is outside of, 0-1.
        """
        self.state = -1
        self.servoYaw = Servo(pin=yaw_pin, min_angle=0, max_angle=180)
        self.servoPitch = Servo(pin=pitch_pin, min_angle=0, max_angle=180)
        self.camera = Camera(camera_index=camera_index)
        self.displayFeed = displayFeed
        self.boundingBox = boundingBox
        self.state = 0

    def start(self):
        self.running = True
        self.loop()

    def stop(self):
        self.running = False

    def loop(self):
            try:
                while self.running:
                    if(self.displayFeed):
                        self.camera.displayCamera()
   
                    if self.camera.see_face():
                        self.state = 1
                    else:
                        self.state = 0

                    self.execute_state()
                    if(cv2.waitKey(1) == ord('q')):
                        break
      
            except KeyboardInterrupt:
                self.running = False
                print("\nProgram interrupted by user.")
                
            except Exception as e:
                self.running = False
                print(f"An error occurred: {e}")

            finally:
                self.servoYaw.cleanup()
                self.servoPitch.cleanup()
                self.camera.cleanup()

    def restart(self):
        pass

    def execute_state(self):
        if self.state == 0:
            self.search()
        elif self.state == 1:
            self.follow()

    def search(self):
        '''Implement iterative search'''
        pass

    def follow(self):
        dir = self.camera.get_face_direction_from_origin()

        # check x-coord
        if (dir[0] != 0):        
            if(dir[0] < (1-self.boundingBox)*self.camera.width/2):
                self.servoYaw.update_angle(90*dir[0]/(self.camera.width/2))
            elif(dir[0] > (1+self.boundingBox)*self.camera.width/2):
                self.servoYaw.update_angle(90*dir[0]/(self.camera.width/2))
        # check y-coord
        if(dir[1] != 0):
            if(dir[0] < (1-self.boundingBox)*self.camera.height/2):
                self.servoPitch.update_angle(90*dir[1]/(self.camera.height/2))
            elif(dir[0] > (1+self.boundingBox)*self.camera.height/2):
                self.servoPitch.update_angle(90*dir[1]/(self.camera.height/2))
