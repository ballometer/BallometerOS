try:
    import RPi.GPIO as GPIO
except ImportError:
    pass

import time


class Buttons:

    def __init__(self):
        self._left = 9
        self._up = 27
        self._right = 22
        self._down = 10
        self._a = 18
        self._b = 25

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self._left, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._right, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self._b, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @property
    def up(self):
        return not GPIO.input(self._up)

    @property
    def down(self):
        return not GPIO.input(self._down)

    @property
    def left(self):
        return not GPIO.input(self._left)

    @property
    def right(self):
        return not GPIO.input(self._right)

    @property
    def a(self):
        return not GPIO.input(self._a)

    @property
    def b(self):
        return not GPIO.input(self._b)

    @property
    def any(self):
        return self.up or self.down or self.left or self.right or self.a or self.b

    @property
    def yes(self):
        return self.a or self.right

    @property
    def no(self):
        return self.b or self.left

    def await_unclick(self):
        while self.any:
            time.sleep(0.001)
