import ballometer
import time

bmp = ballometer.BMP()
sht = ballometer.SHT()
tsl = ballometer.TSL()
lsm = ballometer.LSM()

store = ballometer.Store()

while True:
    keys = []
    values = []
    
    keys.append('bmp_pressure')
    values.append(bmp.pressure)
    keys.append('bmp_temperature')
    values.append(bmp.temperature)

    keys.append('sht_temperature')
    values.append(sht.temperature)
    keys.append('sht_humidity')
    values.append(sht.humidity)

    keys.append('tsl_visible')
    values.append(tsl.visible)
    keys.append('tsl_infrared')
    values.append(tsl.infrared)

    keys.append('lsm_accel_x')
    values.append(lsm.accel_x)
    keys.append('lsm_accel_y')
    values.append(lsm.accel_y)
    keys.append('lsm_accel_z')
    values.append(lsm.accel_z)

    keys.append('lsm_mag_x')
    values.append(lsm.mag_x)
    keys.append('lsm_mag_y')
    values.append(lsm.mag_y)
    keys.append('lsm_mag_z')
    values.append(lsm.mag_z)
    
    store.multi_save(keys=keys, values=values)

    time.sleep(0.7)  # loop execution takes 200 ms
