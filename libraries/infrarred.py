from machine import Pin


class Infrared:
    def __init__(self, pin: int):
        self.pin_value = pin
        self.pin = Pin(pin, Pin.IN)

    def read(self, invert: bool = True) -> int:
        # Read the value of the infrared sensor
        if invert:
            return not self.pin.value()
        else:
            return self.pin.value()
    
    def get_pin_value(self) -> int:
        # Get the pin value
        return self.pin_value