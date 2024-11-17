import lgpio
import time

class Servo:
    def __init__(self, chip, pin, min_angle=0, max_angle=180):
        """
        Initialize a servo motor.
        
        :param chip: GPIO chip number (usually 0 for Raspberry Pi).
        :param pin: GPIO pin number connected to the servo signal wire.
        :param min_angle: Minimum angle for the servo (default: 0).
        :param max_angle: Maximum angle for the servo (default: 180).
        """
        self.chip = chip
        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.current_angle = 90  # Default starting angle

        # Initialize the chip and GPIO pin
        self.handle = lgpio.gpiochip_open(self.chip)
        lgpio.gpio_claim_output(self.handle, self.pin)

        self.pwm_freq = 50  # 50Hz PWM frequency
        self.set_angle(self.current_angle)

    def angle_to_pulse_width(self, angle):
        """
        Convert an angle to a pulse width (duty cycle percentage).
        :param angle: Desired angle in degrees.
        :return: Corresponding pulse width in microseconds.
        """
        return 500 + (angle / 180.0) * 2000  # Maps 0-180 to 500-2500 µs

    def set_angle(self, angle):
        """
        Set the servo to a specific angle.
        :param angle: Target angle in degrees.
        """
        angle = max(self.min_angle, min(self.max_angle, angle))  # Clamp angle
        pulse_width = self.angle_to_pulse_width(angle)
        lgpio.tx_pulse(self.handle, self.pin, pulse_width, 20000 - pulse_width)  # Send PWM signal
        time.sleep(0.5)  # Allow time for the servo to move
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
        Release the GPIO pin and close the chip.
        """
        lgpio.gpiochip_close(self.handle)
