from machine import Pin, PWM


class Servo:
    """
    ESP32-friendly MicroPython servo driver.

    Supports:
    - Standard servos (0-180°)
    - Continuous rotation servos (-100 to 100 speed)

    Uses duty_ns() when available for more accurate pulse timing on ESP32.
    """

    def __init__(
        self,
        pin: int,
        freq: int = 50,
        continuous: bool = False,
        min_us: int = 500,
        max_us: int = 2500,
        neutral_us: int = 1500,
    ):
        self.pin = pin
        self.freq = freq
        self.continuous = continuous

        self.min_us = min_us
        self.max_us = max_us
        self.neutral_us = neutral_us

        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)

    # -------------------------------------------------
    # Internal helpers
    # -------------------------------------------------

    def _write_us(self, pulse_us: int):
        """
        Write pulse width in microseconds.
        ESP32 MicroPython supports duty_ns(), which is
        much more precise than duty().
        """
        pulse_us = max(self.min_us, min(self.max_us, pulse_us))

        # Convert microseconds to nanoseconds
        self.pwm.duty_ns(pulse_us * 1000)

    # -------------------------------------------------
    # Standard servo control
    # -------------------------------------------------

    def angle(self, degrees: float):
        """
        Move standard servo to angle.

        degrees: 0 to 180
        """
        if self.continuous:
            raise ValueError("Use speed() for continuous servos")

        degrees = max(0, min(180, degrees))

        pulse = self.min_us + (
            (self.max_us - self.min_us) * (degrees / 180)
        )

        self._write_us(int(pulse))

    # -------------------------------------------------
    # Continuous servo control
    # -------------------------------------------------

    def speed(self, value: int):
        """
        Set continuous servo speed.

        value:
            -100 = full reverse
             0   = stop
             100 = full forward
        """
        if not self.continuous:
            raise ValueError("Use angle() for standard servos")

        value = max(-100, min(100, value))

        # Typical continuous servo range:
        # 1000us = reverse
        # 1500us = stop
        # 2000us = forward
        pulse = self.neutral_us + (value * 5)

        self._write_us(int(pulse))

    def stop(self):
        """Stop continuous servo."""
        if self.continuous:
            self.speed(0)

    def deinit(self):
        """Turn off PWM."""
        self.pwm.deinit()