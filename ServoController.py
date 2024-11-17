from gpiozero import AngularServo
import math

class Servo:
    def __init__(self, pin:int, min_angle:int=0, max_angle:int=180):
        """
        Initialize a servo motor.
        
        :param pin: GPIO pin number connected to the servo signal wire.
        :param min_angle: Minimum angle for the servo (default: 0).
        :param max_angle: Maximum angle for the servo (default: 180).
        """
        self.servo = AngularServo(pin=pin, min_angle=min_angle, max_angle=max_angle, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

    def set_angle(self, angle:int):
        """
        Set the servo to a specific angle.
        :param angle: Target angle in degrees.
        """
        try:
            angle = max(self.servo.min_angle, min(self.servo.max_angle, angle))  # Clamp angle  
        except Exception as e:
            print(e)
            return
        self.servo.angle = angle
        '''
        pulse_width = self.angle_to_pulse_width(angle)
        for _ in range(25):
            lgpio.tx_pulse(self.handle, self.pin, pulse_width, 20000 - pulse_width)  # Send PWM signal
            time.sleep(0.02)  # Allow time for the servo to move

        self.current_angle = angle
        '''
    
    def set_value(self, value):
        try:
            pass
            #value = max(1, min(-1, value))  # Clamp angle  
        except Exception as e:
            print(e)
            return
        self.servo.value = value
            

    def update_angle(self, delta=0, speed=0):
        """
        Increment or decrement the servo angle.
        :param delta: Change in angle (positive or negative).
        :param speed: Delay between steps (seconds, default: 0 for instant update).
        """
        if math.abs(delta) < 10:
            # angle too small
            print(f"Cannot adjust too small angle {delta}")
            return
        self.set_angle(self.servo.angle + delta)

    def get_angle(self):
        return self.servo.angle

    def cleanup(self):
        """
        Release the GPIO pin and close the chip.
        """
        self.servo.close()
