import ballometer


def test_visible():
    tsl = ballometer.TSL()
    assert 0.0 <= tsl.visible


def test_infrared():
    tsl = ballometer.TSL()
    assert 0.0 <= tsl.infrared


def test_all():
    print('test_visible()')
    test_visible()
    print('test_infrared()')
    test_infrared()


if __name__ == '__main__':
    test_all()
