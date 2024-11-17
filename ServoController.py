import RPi.GPIO as GPIO
import time


class Servo:
    def __init__(self, pin, min_angle=0, max_angle=180):
        """
        Initialize a servo motor.

        :param pin: GPIO pin connected to the servo signal wire.
        :param min_angle: Minimum angle for the servo (default: 0).
        :param max_angle: Maximum angle for the servo (default: 180).
        """
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = 90  # Default starting angle
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 50)  # 50Hz frequency for standard servos
        self.pwm.start(0)
        self.set_angle(self.current_angle)

    def angle_to_duty_cycle(self, angle):
        """
        Convert angle to duty cycle.
        :param angle: Desired angle in degrees.
        :return: Corresponding duty cycle.
        """
        return 2 + (angle / 18)  # Maps 0-180 to 2-12 duty cycle

    def set_angle(self, angle):
        """
        Set the servo to a specific angle.
        :param angle: Target angle in degrees.
        """
        angle = max(self.min_angle, min(self.max_angle, angle))  # Clamp angle
        duty = self.angle_to_duty_cycle(angle)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)  # Allow time for the servo to move
        self.pwm.ChangeDutyCycle(0)  # Stop the PWM signal
        self.current_angle = angle

    def update_angle(self, delta, speed=0):
        """
        Increment or decrement the servo angle.
        :param delta: Change in angle (positive or negative).
        :param speed: Delay between steps (seconds, default: 0 for instant update).
        """
        target_angle = self.current_angle + delta
        target_angle = max(self.min_angle, min(self.max_angle, target_angle))  # Clamp target angle
        step = 1 if delta > 0 else -1

        for angle in range(self.current_angle, target_angle + step, step):
            self.set_angle(angle)
            if speed > 0:
                time.sleep(speed)

    def cleanup(self):
        """
        Stop the PWM signal and cleanup GPIO resources.
        """
        self.pwm.stop()
        GPIO.cleanup()

