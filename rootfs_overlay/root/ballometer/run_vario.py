import redis
import ballometer
import json
import time


store = ballometer.Store()
r = redis.Redis()
vario = ballometer.Vario()

p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe('save:bmp_pressure')

ignore_speed_until = time.time() + 10  # s

qnh_old = store.qnh
qnh_now = qnh_old

for message in p.listen():
    
    qnh_now = store.qnh
    if qnh_now != qnh_old:
        # reset Kalman filter
        vario = ballometer.Vario()
        ignore_speed_until = time.time() + 10  # s
        qnh_old = qnh_now

    vario.qnh_pa = qnh_now * 1e2  # Pa
    data = json.loads(message['data'])
    unixtime = data['unixtime']  # seconds
    vario.pressure = data['value']  # Pa
    altitude = vario.altitude  # m
    speed = vario.speed  # m/s
    if time.time() < ignore_speed_until:
        speed = 0.0

    store.save(key='vario_altitude', value=altitude, unixtime=unixtime)
    store.save(key='vario_speed', value=speed, unixtime=unixtime)
