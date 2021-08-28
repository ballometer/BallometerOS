try:
    from adafruit_gps import GPS as ada_gps
    import serial
except ImportError:
    class ada_gps:
        pass


class GPS(ada_gps):
    def __init__(self):
        uart = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=10)
        super().__init__(uart, debug=False)
        self.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        self.send_command(b"PMTK220,1000")
