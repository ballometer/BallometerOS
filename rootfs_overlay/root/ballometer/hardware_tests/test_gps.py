import ballometer
import time


def test_all():
    gps = ballometer.GPS()

    while True:
        gps.update()
        if gps.timestamp_utc is not None:
            t = time.mktime(gps.timestamp_utc)
            if t > 0:
                break
        time.sleep(0.1)


if __name__ == '__main__':
    test_all()
