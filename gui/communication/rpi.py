"""
This module interfaces the GUI with the GPIO.
"""

try:
    import RPi.GPIO as GPIO

    def configure():
        """
        Configures the pins.

        Call this function only once per **program**
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)

    def start_alarm_system():
        """
        Raises the LED and buzzer alarm
        """

        GPIO.setmode(GPIO.BCM)
        GPIO.output(17, GPIO.HIGH)

    def stop_alarm_system():
        """
        Lowers the LED and buzzer alarm
        """

        GPIO.setmode(GPIO.BCM)
        GPIO.output(17, GPIO.LOW)

except (ImportError, RuntimeError):
    def configure():
        """
        Configures the pins.

        Call this function only once per **program**
        """
        print("rpi.configure - fake function")

    def start_alarm_system():
        """
        Raises the LED and buzzer alarm
        """
        print("rpi.stop_alarm_system - fake function")

    def stop_alarm_system():
        """
        Lowers the LED and buzzer alarm
        """
        print("rpi.stop_alarm_system - fake function")
