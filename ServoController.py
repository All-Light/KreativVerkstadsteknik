from gpiozero import AngularServo
import time

class Servo:
    def __init__(self, pin:int, min_angle:int=0, max_angle:int=180, debug:bool=False):
        """
        Initialize a servo motor.
        
        :param pin: GPIO pin number connected to the servo signal wire.
        :param min_angle: Minimum angle for the servo (default: 0).
        :param max_angle: Maximum angle for the servo (default: 180).
        """
        self.debug = debug
        self.next_angle = 0
        try: 
            self.servo = AngularServo(pin=pin, min_angle=min_angle, max_angle=max_angle)
        except Exception as e:
            raise IOError(f"Cannot open servo at pin {pin}")

    def set_angle(self, angle:int, delay):
        """
        Set the servo to a specific angle.
        :param angle: Target angle in degrees.
        """
        try:
            angle = max(self.servo.min_angle, min(self.servo.max_angle, angle))  # Clamp angle  
        except Exception as e:
            print(e)
            return
        #if(self.debug):
        #    print(f"<{self}> updating angle: {angle}")
        self.next_angle = angle
        time.sleep(delay)
   
    def set_value(self, value):
        try:
            pass
            #value = max(1, min(-1, value))  # Clamp angle  
        except Exception as e:
            print(e)
            return
        self.servo.value = value
            

    def update_angle(self, delta=0, delay=0):
        """
        Increment or decrement the servo angle.
        :param delta: Change in angle (positive or negative).
        :param speed: Delay between steps (seconds, default: 0 for instant update).
        """
        if abs(delta) < 3:
            # angle too small
            print(f"Cannot adjust too small angle {delta}")
            return
        self.set_angle(self.servo.angle + delta, delay)

    def get_angle(self):
        return self.servo.angle

    def get_internal_angle(self):
        return self.next_angle

    def cleanup(self):
        """
        Release the GPIO pin and close the chip.
        """
        self.servo.close()

    def force_angle(self,angle):
        self.servo.angle = angle
