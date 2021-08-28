try:
    import busio
    import adafruit_tsl2591
except ImportError:
    pass


class TSL:
    def __init__(self):
        self._sensor = adafruit_tsl2591.TSL2591(i2c=busio.I2C(24, 23))
        self._sensor.gain = adafruit_tsl2591.GAIN_LOW

    @property
    def visible(self):
        '''returns the visible channel in arbitrary units'''
        return float(self._sensor.visible)

    @property
    def infrared(self):
        '''returns the infrared channel in arbitrary units'''
        return float(self._sensor.infrared)
