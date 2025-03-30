import cv2
import time
from picamera2 import Picamera2

class Camera:
    def __init__(self, using_rpiCam=True, camera_index=0, cascade_path="haarcascade_frontalface_default.xml", debug:bool=False):
        """
        Initialize the camera controller.

        :param camera_index: Index of the camera (default: 0 for primary camera).
        :param cascade_path: Path to the Haar cascade XML file for face detection.
        """
        self.camera_index = camera_index
        self.cascade = cv2.CascadeClassifier(cascade_path)

        self.using_rpiCam = using_rpiCam
        if using_rpiCam:
            self.cap = Picamera2()
            self.width = 1280#1280#640
            self.height = 720#720#480
            self.cap.configure(self.cap.create_video_configuration(main={ "size": (self.width, self.height)}))
            self.cap.start()

        else:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            if not self.cap.isOpened():
                raise IOError(f"Cannot open camera with index {camera_index}")
        
        self.prev_time = 0 # used for FPS
        self.debug = debug

    def get_frame(self):
        """
        Capture a frame from the camera.
        :return: The frame as a numpy array (BGR format), or None if the frame couldn't be read.
        """
        if self.using_rpiCam:
            frame_raw = self.cap.capture_array()
            if frame_raw is None:
                print("Error: Failed to capture frame.")
                return None
            
            #print(f"Captured frame with shape: {frame_raw.shape} and dtype: {frame_raw.dtype}")
            frame = cv2.cvtColor(frame_raw, cv2.COLOR_RGB2BGR)
            
        else:
            ret, frame = self.cap.read()
            if not ret:
                return None
        return frame
    
    def get_fps(self):
        """
        Calculates the current frames per second in the video feed.
        :return: The current FPS
        """
        current_time = time.perf_counter()
        fps = 1 / (current_time - self.prev_time) if self.prev_time else 0

        self.prev_time = current_time

        # Convert FPS to integer for display
        return int(fps)

    def detect_face(self, frame):
        """
        Detect faces in a given frame.
        :param frame: A single frame (numpy array) to process.
        :return: List of face bounding boxes [(x, y, w, h), ...].
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale for detection
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return faces

    def see_face(self):
        """
        Check if a face is detected in the current camera feed.
        :return: True if a face is detected, False otherwise.
        """
        frame = self.get_frame()
        if frame is None:
            return False
        faces = self.detect_face(frame)
        return len(faces) > 0

    def get_face_coordinates(self):
        """
        Get the coordinates of detected faces in the current frame.
        :return: List of face bounding boxes [(x, y, w, h), ...].
        """
        frame = self.get_frame()
        if frame is None:
            return []
        return self.detect_face(frame)
    
    def origin_offset_coordinates(self, x, y):
        """
        Offsets the coordinates by half the width or height to reorient 0,0 to be middle of camera
        """
        return [(x-self.width/2), int(y-self.height/2)]

    def get_face_direction_from_origin(self, id=0):
        """
        Gets the direction of where the face is located in relation to the middle of the screen.
        Note that y-coordinates is negative when going upwards
        """
        faces = self.get_face_coordinates()
        if(len(faces) < 1):
            return [0,0]
        x, y, w, h = faces[id]
        x, y = self.origin_offset_coordinates(x+w/2,y+h/2)

        return [x,y]

    def displayCamera(self):
        frame = self.get_frame()
        if frame is None:
            print("Failed to capture frame.")
            return
        
        faces = self.detect_face(frame)
        if len(faces) > 0:
            for id, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
                cv2.putText(frame, f"Face ID: {id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        
        cv2.putText(frame, f"FPS: {self.get_fps()}", (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2, cv2.LINE_AA)
        cv2.imshow("Camera Feed", frame)

    def cleanup(self):
        """
        Release the camera and close any open OpenCV windows.
        """
        if not self.using_rpiCam:
            self.cap.release()
        cv2.destroyAllWindows()
