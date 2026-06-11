import time
from machine import Pin
from machine import time_pulse_us


class Ultrasound:
    def __init__(self, trigger: int, echo: int):
        self.trigger_pin = trigger
        self.echo_pin = echo
        self.trigger = Pin(trigger, Pin.OUT)
        self.echo = Pin(echo, Pin.IN)
    
    def get_distance(self) -> int:
        # Get the distance from the ultrasound sensor
        self.trigger.off()
        time.sleep_us(2)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        sound_speed = 0.0343 # 343 m/s but converted in cm/us
        duration = time_pulse_us(self.echo, 1) # in microseconds (us)
        distance = (duration * sound_speed) / 2 # distance is double from object
        distance = int(distance)

        return distance
    
    def get_trigger_pin(self) -> int:
        # Get the trigger pin
        return self.trigger_pin
    
    def get_echo_pin(self) -> int:
        # Get the echo pin
        return self.echo_pin