import ballometer


def test_temperature():
    sht = ballometer.SHT()
    assert 250 < sht.temperature < 350


def test_humidity():
    sht = ballometer.SHT()
    assert 0 <= sht.humidity <= 100


def test_all():
    print('test_temperature()')
    test_temperature()
    print('test_humidity()')
    test_humidity()


if __name__ == '__main__':
    test_all()
