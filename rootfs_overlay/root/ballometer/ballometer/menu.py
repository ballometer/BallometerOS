import time
import datetime
import json
from . import wifi as w
from . import update as u
from . import metar as m
import ballometer


def _choose(lcd, buttons, items=['item1', 'item2']):
    i = 0
    if len(items) == 0:
        return i

    while True:
        lcd.cursor_pos = (1, 0)
        text = '>' + items[i]
        text += ' ' * (lcd.columns - len(text))
        lcd.write_string(text)

        buttons.await_unclick()

        while True:

            if (i > 0) and buttons.up:
                i -= 1
                break

            if (i < len(items) - 1) and buttons.down:
                i += 1
                break

            if buttons.yes or buttons.no:
                return i


def startup(params):
    lcd = params['lcd']

    lcd.clear()
    
    def get_username_password():
        username = 'default-user-name'
        password = 'default-password'

        try:
            # this file should look like
            # {
            #     "username": "your-username",
            #     "password": "your-password"
            # }
            with open('/data/credentials.json') as f:
                credentials = json.load(f)
                username = credentials['username']
                password = credentials['password']
                
        except json.decoder.JSONDecodeError as e:
            print('json.decoder.JSONDecodeError ' + format(e))
        except FileNotFoundError as e:
            print('FileNotFoundError ' + format(e))
        except KeyError as e:
            print('KeyError ' + format(e))
            
        return username, password
    
    username, _ = get_username_password()
    
    lcd.write_string('BALLOMETER:\r\nHOI ' + username.upper())
    time.sleep(3.0)

    lcd.clear()
    lcd.write_string('RELEASE\r\n' + u.get_installed_release())
    time.sleep(1.5)

    return home, params


def home(params):
    lcd = params['lcd']
    buttons = params['buttons']

    metar_done = params['metar_done']

    store = ballometer.Store()
    
    lcd.clear()
    lcd.cursor_pos = (0, 0)

    lcd.write_string('\r\n>MENU')
    
    check_interval = 10  # s
    last_check = 0
    last_ip = ''

    buttons.await_unclick()

    while not buttons.yes:
        if last_check + check_interval < time.time():
            if not metar_done:
                data = m.get_metar(store.qnh_station_id)
                if data != {}:
                    return metar, params

            ip = w.get_ip()

            if ip != last_ip:
                last_ip = ip
                lcd.cursor_pos = (0, 0)
                text = ip
                text += ' ' * (lcd.columns - len(text))
                lcd.write_string(text)

            if store.recording:
                lcd.cursor_pos = (1, 12)
                lcd.write_string('REC*')
            else:
                lcd.cursor_pos = (1, 12)
                lcd.write_string('    ')

            last_check = time.time()

    return menu, params


def menu(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('MENU')

    items = ['QNH', 'REC', 'WIFI', 'UPDATE']
    item = items[_choose(lcd=lcd, buttons=buttons, items=items)]

    if buttons.no:
        return home, params

    if item == 'QNH':
        return qnh, params

    if item == 'REC':
        return rec, params

    if item == 'WIFI':
        return wifi, params

    return update, params


def rec(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('REC')

    items = ['START', 'CONTINUE', 'STOP']

    buttons.await_unclick()

    item = items[_choose(lcd=lcd, buttons=buttons, items=items)]

    if buttons.no:
        return menu, params

    
    store = ballometer.Store()

    if item == 'START':
        lcd.clear()
        lcd.write_string('WAITING FOR GPS\r\nOR INTERNET TIME')
        time.sleep(1.0)
        while not store.clock_was_synchronized():
            time.sleep(1.0)
            if buttons.no:
                lcd.clear()
                lcd.write_string('CANCEL...')
                time.sleep(2.0)
                return home, params

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('START REC...')
        store.flight_id += 1
        store.recording = True
        lcd.cursor_pos = (1, 0)
        lcd.write_string('FLIGHT ID %i' % store.flight_id)
        time.sleep(2.0)
            
        return home, params

    if item == 'CONTINUE':
        lcd.clear()
        lcd.write_string('WAITING FOR GPS\r\nOR INTERNET TIME')
        time.sleep(1.0)
        while not store.clock_was_synchronized():
            time.sleep(1.0)
            if buttons.no:
                lcd.clear()
                lcd.write_string('CANCEL...')
                time.sleep(2.0)
                return home, params

        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('CONTINUE REC...')
        store.recording = True
        lcd.cursor_pos = (1, 0)
        lcd.write_string('FLIGHT ID %i' % store.flight_id)
        time.sleep(2.0)
            
        return home, params

    if item == 'STOP':
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string('STOP REC...')
        store.recording = False
        lcd.cursor_pos = (1, 0)
        lcd.write_string('FLIGHT ID %i' % store.flight_id)
        time.sleep(2.0)
        return home, params
    
    return home, params


def qnh(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('QNH')

    items = ['GET', 'SET', 'AIRPORT']

    buttons.await_unclick()

    item = items[_choose(lcd=lcd, buttons=buttons, items=items)]

    if buttons.no:
        return menu, params

    if item == 'GET':
        return qnh_get, params

    if item == 'SET':
        return qnh_set, params

    if item == 'AIRPORT':
        return qnh_airport, params

    return home, params


def qnh_get(params):
    lcd = params['lcd']
    buttons = params['buttons']
    store = ballometer.Store()
    last_qnh = '%04i' % int(store.qnh)

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'QNH:\r\n' + last_qnh
    lcd.write_string(text)

    buttons.await_unclick()

    while True:
        if buttons.yes or buttons.no:
            break
        time.sleep(0.05)
    
    if buttons.yes:
        return home, params
    else:
        return qnh, params

    
def qnh_set(params):
    lcd = params['lcd']
    buttons = params['buttons']
    store = ballometer.Store()
    last_qnh = '%04i' % int(store.qnh)

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'QNH:\r\n' + last_qnh
    lcd.write_string(text)

    cursor = 3
    shift = 0

    lcd.cursor_mode = 'line'
    lcd.cursor_pos = (1, cursor)
    buttons.await_unclick()

    letters = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ]

    text_max_length = 4
    text_codes = [letters.index(letter) for letter in last_qnh]

    while True:
        while True:
            begin_press = True
            while buttons.up:
                text_codes[cursor + shift] = text_codes[cursor + shift] + 1
                text_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[text_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            while buttons.down:
                text_codes[cursor + shift] = text_codes[cursor + shift] - 1
                text_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[text_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            if buttons.left:
                if cursor > 0:
                    cursor -= 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift > 0:
                    shift -= 1
                    lcd.cursor_pos = (1, 0)
                    tmp = text_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.right:
                if cursor < text_max_length - 1:
                    cursor += 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift < text_max_length - 1:
                    shift += 1
                    lcd.cursor_pos = (1, 0)
                    tmp = text_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.a or buttons.b:
                break

        if buttons.a or buttons.b:
            break

    lcd.cursor_mode = 'hide'
    lcd.clear()
    lcd.cursor_pos = (0, 0)

    if buttons.no:
        return qnh, params

    qnh_new = int(''.join([letters[code] for code in text_codes]).strip())

    if not (800 < qnh_new < 1200):
        lcd.write_string('OUT OF RANGE\r\n800 < QNH < 1200')
        time.sleep(2.0)
        return qnh_set, params

    lcd.write_string('SETTING QNH...')
    store.qnh = qnh_new
    time.sleep(1.0)

    return home, params

def qnh_airport(params):
    lcd = params['lcd']
    buttons = params['buttons']
    store = ballometer.Store()

    lcd.clear()
    lcd.cursor_pos = (0, 0)

    station_id = store.qnh_station_id
    text = f'CHOOSE AIRPORT:\r\n{station_id}'
    lcd.write_string(text)

    cursor = 3
    shift = 0

    lcd.cursor_mode = 'line'
    lcd.cursor_pos = (1, cursor)
    buttons.await_unclick()

    letters = [
        ' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 
        'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9',
    ]

    text_max_length = 4
    text_codes = [letters.index(letter) for letter in station_id]

    while True:
        while True:
            begin_press = True
            while buttons.up:
                text_codes[cursor + shift] = text_codes[cursor + shift] + 1
                text_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[text_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            while buttons.down:
                text_codes[cursor + shift] = text_codes[cursor + shift] - 1
                text_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[text_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            if buttons.left:
                if cursor > 0:
                    cursor -= 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift > 0:
                    shift -= 1
                    lcd.cursor_pos = (1, 0)
                    tmp = text_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.right:
                if cursor < text_max_length - 1:
                    cursor += 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift < text_max_length - 1:
                    shift += 1
                    lcd.cursor_pos = (1, 0)
                    tmp = text_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.a or buttons.b:
                break

        if buttons.a or buttons.b:
            break

    lcd.cursor_mode = 'hide'
    lcd.clear()
    lcd.cursor_pos = (0, 0)

    if buttons.no:
        return qnh, params

    station_id_new = ''.join([letters[code] for code in text_codes]).strip()

    data = m.get_metar(station_id_new)

    if data == {}:
        lcd.write_string(f'AIRPORT {station_id_new}\r\nNOT FOUND...')
        time.sleep(3.0)
        return home, params

    lcd.write_string(f'AIRPORT FOUND:\r\n{data["station_id"]}')
    store.qnh_station_id = station_id_new
    time.sleep(3.0)

    return metar, params


def wifi(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('WIFI')

    items = ['ADD', 'DELETE', 'RESET']

    buttons.await_unclick()

    item = items[_choose(lcd=lcd, buttons=buttons, items=items)]

    if buttons.no:
        return menu, params

    if item == 'ADD':
        return wifi_add, params

    if item == 'DELETE':
        return wifi_delete, params

    return wifi_reset, params


def wifi_add(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('SCANNING...')

    ssids = w.scan()

    if len(ssids) == 0:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'NO WIFI\r\nFOUND...'
        lcd.write_string(text)
        time.sleep(2)
        return wifi, params

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'CHOOSE WIFI:'
    lcd.write_string(text)

    ssids_decoded = [w.decode_name(name) for name in ssids]

    i = _choose(lcd=lcd, buttons=buttons, items=ssids_decoded)

    if buttons.no:
        return wifi, params

    params['ssid'] = ssids[i]
    return wifi_password, params


def wifi_password(params):
    lcd = params['lcd']
    buttons = params['buttons']
    ssid = params['ssid']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'PASSWORD:'
    lcd.write_string(text)

    password_max_length = 64
    password_codes = [0 for _ in range(password_max_length)]

    cursor = 0
    shift = 0

    lcd.cursor_mode = 'line'
    lcd.cursor_pos = (1, cursor)
    buttons.await_unclick()

    letters = [
        ' ',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '.', ',', '?', '!',
        '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', '-', '/', ':', ';',
        '<', '=', '>', '@', '[', ']', '^', '_', '`', '{', '|', '}', '0', '1',
        '2', '3', '4', '5', '6', '7', '8', '9',
    ]

    while True:
        while True:
            begin_press = True
            while buttons.up:
                password_codes[cursor +
                               shift] = password_codes[cursor + shift] + 1
                password_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[password_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            while buttons.down:
                password_codes[cursor +
                               shift] = password_codes[cursor + shift] - 1
                password_codes[cursor + shift] %= len(letters)
                lcd.write_string(letters[password_codes[cursor + shift]])
                lcd.cursor_pos = (1, cursor)

                if begin_press:
                    time.sleep(0.2)
                    begin_press = False
                else:
                    time.sleep(0.05)

            if buttons.left:
                if cursor > 0:
                    cursor -= 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift > 0:
                    shift -= 1
                    lcd.cursor_pos = (1, 0)
                    tmp = password_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.right:
                if cursor < lcd.columns - 1:
                    cursor += 1
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break
                elif cursor + shift < password_max_length - 1:
                    shift += 1
                    lcd.cursor_pos = (1, 0)
                    tmp = password_codes[shift:(shift + lcd.columns)]
                    text = ''.join([letters[code] for code in tmp])
                    lcd.write_string(text)
                    lcd.cursor_pos = (1, cursor)
                    time.sleep(0.3)
                    break

            if buttons.a or buttons.b:
                break

        if buttons.a or buttons.b:
            break

    lcd.cursor_mode = 'hide'
    lcd.clear()
    lcd.cursor_pos = (0, 0)

    if buttons.a:
        lcd.write_string('CONNECTING...')
        time.sleep(0.75)
        password = ''.join([letters[code] for code in password_codes]).strip()
        w.add(ssid, password)
    else:
        lcd.write_string('CANCEL...')
        time.sleep(1)

    return home, params


def wifi_delete(params):
    lcd = params['lcd']
    buttons = params['buttons']

    ssids = w.known()

    if len(ssids) == 0:
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        text = 'NO WIFI\r\nSTORED...'
        lcd.write_string(text)
        time.sleep(2)
        return wifi, params

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'DELETE WIFI:'
    lcd.write_string(text)

    i = _choose(lcd=lcd, buttons=buttons, items=[
                w.decode_name(name) for name in ssids])

    if buttons.no:
        return wifi, params

    w.remove(ssids[i])
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'DELETED:\r\n' + ssids[i]
    lcd.write_string(text)
    time.sleep(2)

    return home, params


def wifi_reset(params):
    lcd = params['lcd']
    buttons = params['buttons']

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'RESET WIFI?'
    lcd.write_string(text)

    items = ['NO', 'YES']
    i = _choose(lcd=lcd, buttons=buttons, items=items)

    if buttons.no or items[i] == 'NO':
        return wifi, params

    lcd.clear()
    lcd.cursor_pos = (0, 0)
    text = 'RESETTING\r\nWIFI...'
    lcd.write_string(text)

    w.reset()

    time.sleep(2)

    return home, params


def update(params):
    lcd = params['lcd']
    buttons = params['buttons']

    try:
        current_release = u.get_installed_release()
    except u.UpdateError:
        lcd.clear()
        lcd.write_string('UPDATE ERROR')
        while not buttons.yes:
            time.sleep(0.01)
        return home, params

    lcd.clear()
    lcd.write_string('RELEASE:\r\n' + current_release)
    time.sleep(2)

    try:
        releases = u.get_available_releases()
    except u.UpdateError:
        lcd.clear()
        lcd.write_string('UPDATE ERROR')
        while not buttons.any:
            time.sleep(0.01)
        return home, params

    if len(releases) == 0:
        lcd.clear()
        lcd.write_string('NO RELEASES\r\nAVAILABLE...')
        time.sleep(2)
        return menu, params

    lcd.clear()
    lcd.write_string('CHOOSE RELEASE\r\n')

    release = releases[_choose(lcd, buttons, releases)]

    if buttons.no:
        return menu, params

    lcd.clear()
    lcd.write_string('INSTALLING...\r\n')

    def update_callback(text):
        lcd.cursor_pos = (1, 0)
        text += ' ' * (lcd.columns - len(text))
        lcd.write_string(text)
        if buttons.no:
            raise u.UpdateError('Abort installation by user')

    try:
        u.install(release=release, update_callback=update_callback)
    except u.UpdateError:
        lcd.clear()
        lcd.write_string('UPDATE ERROR')
        while not buttons.yes:
            time.sleep(0.01)
        return home, params

    while not buttons.any:
        lcd.clear()
        lcd.write_string('UPDATE WAS\r\nSUCESSFUL...')
        for _ in range(200):
            if buttons.any:
                break
            time.sleep(0.01)

        lcd.clear()
        lcd.write_string('PLEASE\r\nRESTART NOW.')
        for _ in range(200):
            if buttons.any:
                break
            time.sleep(0.01)

    return home, params

def metar(params):
    lcd = params['lcd']
    buttons = params['buttons']

    params['metar_done'] = True

    store = ballometer.Store()

    lcd.clear()
    lcd.cursor_pos = (0, 0)

    data = m.get_metar(store.qnh_station_id)

    if data == {}:
        return home, params

    d = datetime.datetime.utcfromtimestamp(data['time'])
    message = f'{data["station_id"]} {d.strftime("%H%MZ")} Q{(data["press"] / 100):.0f}'
    lcd.write_string(f'{message}')

    items = ['COPY QNH', 'MANUAL QNH']
    item = items[_choose(lcd=lcd, buttons=buttons, items=items)]

    if buttons.no:
        return home, params

    if item == 'MANUAL QNH':
        return qnh_set, params

    if item == 'COPY QNH':
        store.qnh = float(data["press"] / 100)
        lcd.clear()
        lcd.cursor_pos = (0, 0)
        lcd.write_string(f'COPIED QNH Q{(data["press"] / 100):.0f}')
        time.sleep(2)
        return home, params

    return home, params
