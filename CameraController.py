import cv2

class Camera:
    def __init__(self, camera_index=0, cascade_path="haarcascade_frontalface_default.xml"):
        """
        Initialize the camera controller.

        :param camera_index: Index of the camera (default: 0 for primary camera).
        :param cascade_path: Path to the Haar cascade XML file for face detection.
        """
        self.camera_index = camera_index
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)
        self.cap = cv2.VideoCapture(self.camera_index)

        if not self.cap.isOpened():
            raise Exception(f"Cannot open camera with index {camera_index}")

    def get_frame(self):
        """
        Capture a frame from the camera.
        :return: The frame as a numpy array (BGR format), or None if the frame couldn't be read.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

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
    
    def displayCamera(self):
        frame = self.get_frame()
        if frame is None:
            print("Failed to capture frame.")
            return
        
        faces = self.detect_face(frame)
        if len(faces) > 0:
            print(f"Detected {len(faces)} face(s): {faces}")
            for id, (x, y, w, h) in enumerate(faces):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
                cv2.putText(frame, f"Face ID: {id}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
        
        cv2.imshow("Camera Feed", frame)

    def cleanup(self):
        """
        Release the camera and close any open OpenCV windows.
        """
        self.cap.release()
        cv2.destroyAllWindows()
