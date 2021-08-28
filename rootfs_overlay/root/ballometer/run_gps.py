import ballometer
import time
import subprocess


def set_system_time(unixtime=1601116701):
    subprocess.run(['date', '-s', '@%i' % int(unixtime)],
                   stdout=subprocess.PIPE).stdout.decode('utf-8')


gps = ballometer.GPS()

time_was_set = False
while not time_was_set:
    gps.update()
    if gps.timestamp_utc is not None:
        t = time.mktime(gps.timestamp_utc)
        if t > 0:
            set_system_time(t)
            time_was_set = True

store = ballometer.Store()

last_write = 0

while True:
    gps.update()
    # loop execution takes 35 ms
    if gps.has_fix and time.time() > last_write + 0.8:
        keys = []
        values = []
        if gps.latitude is not None:
            keys.append('gps_latitude')
            values.append(gps.latitude)

        if gps.longitude is not None:
            keys.append('gps_longitude')
            values.append(gps.longitude)
        
        if gps.altitude_m is not None:
            keys.append('gps_altitude')
            values.append(gps.altitude_m)

        if gps.speed_knots is not None:
            speed = gps.speed_knots * 0.514444  # m/s
            keys.append('gps_speed')
            values.append(speed)
       
        if gps.track_angle_deg is not None:
            keys.append('gps_heading')
            values.append(gps.track_angle_deg)

        if gps.satellites is not None:
            keys.append('gps_satellites')
            values.append(gps.satellites)

        if gps.horizontal_dilution is not None:
            keys.append('gps_horizontal_dilution')
            values.append(gps.horizontal_dilution)
        
        store.multi_save(keys=keys, values=values)
        last_write = time.time()