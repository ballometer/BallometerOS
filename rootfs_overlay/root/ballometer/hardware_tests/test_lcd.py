import ballometer


def test_cursor_pos():
    lcd = ballometer.LCD()
    lcd.cursor_pos = (0, 0)


def test_columns():
    lcd = ballometer.LCD()
    assert lcd.columns == 16


def test_cursor_mode():
    lcd = ballometer.LCD()
    assert lcd.cursor_mode == 'hide'
    lcd.cursor_mode = 'hide'


def test_clear():
    lcd = ballometer.LCD()
    lcd.clear()


def test_write_string():
    lcd = ballometer.LCD()
    lcd.write_string('HALLO WELT')


def test_all():
    print('test_cursor_pos()')
    test_cursor_pos()
    print('test_columns()')
    test_columns()
    print('test_cursor_mode()')
    test_cursor_mode()
    print('test_clear()')
    test_clear()
    print('test_write_string()')
    test_write_string()


if __name__ == '__main__':
    test_all()
