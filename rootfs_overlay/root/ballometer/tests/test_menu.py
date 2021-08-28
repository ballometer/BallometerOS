import time
import ballometer.menu


class LCD:
    cursor_pos = (0, 0)
    columns = 16
    cursor_mode = 'hide'

    def clear(self):
        pass

    def write_string(self, message='hi'):
        pass


def get_ip():
    return '10.0.0.58'


def scan():
    return []


def decode_name(name):
    return name


def add(ssid, password):
    pass


def known():
    return []


def remove(ssid):
    pass


def reset():
    pass


class Buttons:
    def __init__(self):
        self._tic = time.time()

    def await_unclick(self):
        while self.yes or self.no or self.up or self.down:
            time.sleep(0.001)

    @property
    def a(self):
        return False

    @property
    def b(self):
        return False

    @property
    def up(self):
        return False

    @property
    def down(self):
        return False

    @property
    def left(self):
        return False

    @property
    def right(self):
        return False

    @property
    def yes(self):
        return self.right or self.a

    @property
    def no(self):
        return self.left or self.b

    @property
    def any(self):
        return self.up or self.down or self.left or self.right or \
            self.a or self.b


class UpdateError(Exception):
    pass


def get_releases():
    return []


def install(release='v1.0.0', update_callback=lambda text: ()):
    pass


def test_startup(mocker):
    mocker.patch('ballometer.update.get_current_release')
    fn, _ = ballometer.menu.startup({'lcd': LCD()})
    assert fn == ballometer.menu.home


def test_home():
    class B(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.home({'lcd': LCD(), 'buttons': B()})
    assert fn == ballometer.menu.menu


def test_menu():
    class B1(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.menu({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.rec

    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def a(self):
            return self._tic + 0.5 < time.time() < self._tic + 0.6

    fn, _ = ballometer.menu.menu({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.wifi

    class B3(Buttons):
        @property
        def left(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.menu({'lcd': LCD(), 'buttons': B3()})
    assert fn == ballometer.menu.home


def test_rec():
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.rec({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.home

    class B2(Buttons):
        @property
        def b(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.rec({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.menu


def test_wifi():
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.wifi_add

    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def right(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    fn, _ = ballometer.menu.wifi({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.wifi_delete

    class B3(Buttons):
        @property
        def b(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi({'lcd': LCD(), 'buttons': B3()})
    assert fn == ballometer.menu.menu

    class B4(Buttons):
        @property
        def down(self):
            return (self._tic + 0.1 < time.time() < self._tic + 0.2) or \
                (self._tic + 0.3 < time.time() < self._tic + 0.4)

        @property
        def right(self):
            return self._tic + 0.5 < time.time() < self._tic + 0.6

    fn, _ = ballometer.menu.wifi({'lcd': LCD(), 'buttons': B4()})
    assert fn == ballometer.menu.wifi_reset


def test_wifi_add(mocker):
    class B1(Buttons):
        @property
        def right(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi_add({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.wifi

    mocker.patch('ballometer.wifi.scan', return_value=['ssid1', 'ssid2'])

    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def right(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    fn, params_out = ballometer.menu.wifi_add({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.wifi_password
    assert params_out['ssid'] == 'ssid2'

    class B3(Buttons):
        @property
        def left(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi_add({'lcd': LCD(), 'buttons': B3()})
    assert fn == ballometer.menu.wifi


def test_wifi_password(mocker):
    class B1(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    mocker.patch('ballometer.wifi.add')
    fn, _ = ballometer.menu.wifi_password(
        {'lcd': LCD(), 'buttons': B1(), 'ssid': 'ssid1'})
    assert fn == ballometer.menu.home

    class B2(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def a(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    fn, _ = ballometer.menu.wifi_password(
        {'lcd': LCD(), 'buttons': B2(), 'ssid': 'ssid1'})
    assert fn == ballometer.menu.home


def test_wifi_delete(mocker):

    class B1(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def a(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    mocker.patch('ballometer.wifi.remove')
    mocker.patch('ballometer.wifi.known', return_value=['ssid1', 'ssid2'])
    fn, _ = ballometer.menu.wifi_delete({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.home

    class B2(Buttons):
        @property
        def b(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    fn, _ = ballometer.menu.wifi_delete({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.wifi


def test_wifi_reset(mocker):

    mocker.patch('ballometer.wifi.reset')

    class B1(Buttons):
        @property
        def b(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi_reset({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.wifi

    class B2(Buttons):
        @property
        def a(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

    fn, _ = ballometer.menu.wifi_reset({'lcd': LCD(), 'buttons': B2()})
    assert fn == ballometer.menu.wifi

    class B3(Buttons):
        @property
        def down(self):
            return self._tic + 0.1 < time.time() < self._tic + 0.2

        @property
        def a(self):
            return self._tic + 0.3 < time.time() < self._tic + 0.4

    fn, _ = ballometer.menu.wifi_reset({'lcd': LCD(), 'buttons': B3()})
    assert fn == ballometer.menu.home


def test_update(mocker):
    mocker.patch('ballometer.update.get_current_release',
                 return_value='v1.0.0')
    mocker.patch('ballometer.update.get_releases',
                 return_value=['v1.0.0', 'v1.0.1'])

    class B1(Buttons):
        @property
        def b(self):
            return self._tic + 2.3 < time.time() < self._tic + 2.4
    fn, _ = ballometer.menu.update({'lcd': LCD(), 'buttons': B1()})
    assert fn == ballometer.menu.menu
