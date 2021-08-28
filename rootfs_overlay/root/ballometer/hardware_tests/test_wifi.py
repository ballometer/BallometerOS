from ballometer import wifi as w


def test_decode_name():
    assert w.decode_name('t\\xC3\\xA9st') == 'tést'


def test_get_ip():
    assert isinstance(w.get_ip(), str)


def test_scan():
    print('''
    This test assumes that there is an access point with the
    ssid set to "android-ballometer".
    ''')

    assert 'android-ballometer' in w.scan()


def test_add():
    print('''
    This test assumes that there is an access point with the
    ssid set to "android-ballometer" and the password is "abba9889".
    ''')

    w.add(ssid='android-ballometer', password='abba9889')


def test_known():
    print('''
    This test assumes that you have previously added a network with
    ssid "android-ballometer".
    ''')

    assert 'android-ballometer' in w.known()


def test_remove():

    w.remove('android-ballometer')


def test_reset():

    w.reset()


def test_all():
    print('test_decode_name()')
    test_decode_name()
    print('test_get_ip()')
    test_get_ip()
    print('test_scan()')
    test_scan()
    print('test_add()')
    test_add()
    print('test_known()')
    test_known()
    print('test_remove()')
    test_remove()
    print('test_reset()')
    test_reset()


if __name__ == '__main__':
    test_all()
