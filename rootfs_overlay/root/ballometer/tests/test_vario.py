import ballometer


def test_altitude():
    vario = ballometer.Vario()
    vario.pressure = 101325.0  # Pa
    vario.qnh_pa = 101325.0  # Pa
    assert vario.altitude == 0.0
