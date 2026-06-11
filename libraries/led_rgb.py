from machine import Pin, PWM


class LedRGB:
    # Color definitions (RGB 0-255)
    COLORS = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "cyan": (0, 255, 255),
        "magenta": (255, 0, 255),
        "white": (255, 255, 255),
        "off": (0, 0, 0),
        "orange": (255, 165, 0),
        "pink": (255, 192, 203),
        "purple": (128, 0, 128),
        "lime": (0, 255, 0),
        "navy": (0, 0, 128),
        "teal": (0, 128, 128),
        "maroon": (128, 0, 0),
        "olive": (128, 128, 0),
    }
    
    def __init__(self, red_pin: int, green_pin: int, blue_pin: int, freq: int = 1000):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        
        self.red = PWM(Pin(red_pin), freq=freq)
        self.green = PWM(Pin(green_pin), freq=freq)
        self.blue = PWM(Pin(blue_pin), freq=freq)
    
    def set_color(self, red: int, green: int, blue: int):
        """Set the RGB color using values from 0 to 65535"""
        self.red.duty_u16(red)
        self.green.duty_u16(green)
        self.blue.duty_u16(blue)
    
    def set_color_255(self, red: int, green: int, blue: int):
        """Set the RGB color using values from 0 to 255"""
        self.red.duty_u16(int((red / 255) * 65535))
        self.green.duty_u16(int((green / 255) * 65535))
        self.blue.duty_u16(int((blue / 255) * 65535))
    
    def set_color_name(self, color_name: str):
        """Set the RGB color using a color name string"""
        color_name = color_name.lower().strip()
        if color_name in self.COLORS:
            r, g, b = self.COLORS[color_name]
            self.set_color_255(r, g, b)
        else:
            available_colors = ", ".join(self.COLORS.keys())
            raise ValueError(f"Color '{color_name}' not found. Available colors: {available_colors}")
    
    def off(self):
        """Turn off the LED"""
        self.set_color(0, 0, 0)
    
    def get_pins(self) -> tuple:
        """Get the RGB pin numbers"""
        return (self.red_pin, self.green_pin, self.blue_pin)
