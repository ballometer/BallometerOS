try:
    import busio
    import adafruit_lsm303_accel
    import adafruit_lsm303dlh_mag
except ImportError:
    pass


class LSM:
    def __init__(self):
        i2c = busio.I2C(24, 23)
        self._sensor_accel = adafruit_lsm303_accel.LSM303_Accel(
            i2c=i2c, address=0x18)
        self._sensor_mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c=i2c)

    @property
    def accel_x(self):
        '''returns the acceleration in the x-direction in m/s2'''
        return round(self._sensor_accel.acceleration[0], 3)

    @property
    def accel_y(self):
        '''returns the acceleration in the y-direction in m/s2'''
        return round(self._sensor_accel.acceleration[1], 3)

    @property
    def accel_z(self):
        '''returns the acceleration in the z-direction in m/s2'''
        return round(self._sensor_accel.acceleration[2], 3)

    @property
    def mag_x(self):
        '''returns the magnetic field in the x-direction in Tesla'''
        return self._sensor_mag.magnetic[0] * 1e-6

    @property
    def mag_y(self):
        '''returns the magnetic field in the y-direction in Tesla'''
        return self._sensor_mag.magnetic[1] * 1e-6

    @property
    def mag_z(self):
        '''returns the magnetic field in the z-direction in Tesla'''
        return self._sensor_mag.magnetic[2] * 1e-6
