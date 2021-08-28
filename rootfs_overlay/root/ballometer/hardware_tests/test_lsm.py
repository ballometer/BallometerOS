import ballometer


def test_accel_x():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_x < 20.0


def test_accel_y():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_y < 20.0


def test_accel_z():
    lsm = ballometer.LSM()
    assert -20.0 < lsm.accel_z < 20.0


def test_mag_x():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_x < 1e-3


def test_mag_y():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_y < 1e-3


def test_mag_z():
    lsm = ballometer.LSM()
    assert -1e-3 < lsm.mag_z < 1e-3


def test_all():
    print('test_accel_x()')
    test_accel_x()
    print('test_accel_y()')
    test_accel_y()
    print('test_accel_z()')
    test_accel_z()
    print('test_mag_x()')
    test_mag_x()
    print('test_mag_y()')
    test_mag_y()
    print('test_mag_z()')
    test_mag_z()


if __name__ == '__main__':
    test_all()
