try:
    from RPLCD.i2c import CharLCD
except ImportError:
    class CharLCD:
        pass


class LCD(CharLCD):
    def __init__(self):
        super().__init__('PCF8574', 0x27)
        self.columns = 16
