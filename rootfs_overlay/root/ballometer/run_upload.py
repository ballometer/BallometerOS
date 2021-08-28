import ballometer
import json
import requests
import os
import time
import logging


logging.basicConfig(
    filename='/var/log/run_upload.log',
    filemode='a',
    format='%(asctime)s %(levelname)s Line %(lineno)d %(message)s',
    level=ballometer.get_log_level()
)

ballometer_url = os.environ.get('BALLOMETER_URL')
if ballometer_url == None:
    ballometer_url = 'https://api.ballometer.io'
    

logging.info('Starting run_upload...')

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
        logging.info('json.decoder.JSONDecodeError ' + format(e))
    except FileNotFoundError as e:
        logging.info('FileNotFoundError ' + format(e))
    except KeyError as e:
        logging.info('KeyError ' + format(e))
        
    return username, password


def get_jwt_token(username, password):
    token = ''
    
    body = {
        'username': username,
        'password': password
    }
    
    try:
        r = requests.post(ballometer_url + '/auth/login', 
                          json=body, timeout=15)
    except requests.exceptions.ConnectTimeout:
        handle_offline()
        return ''
    except requests.exceptions.ConnectionError:
        handle_offline()
        return ''
    
    if r.status_code == 403:
        handle_wrong_credentials(username, password)
        return ''

    try:
        token = r.json()['token']
    except json.decoder.JSONDecodeError:
        return ''
    except KeyError:
        return ''
    
    return token


def handle_wrong_credentials(username, password):
    # Fire some signal flare to the user that the
    # password or username is wrong.
    logging.info('Wrong credentials')


def handle_offline():
    # Fire some signal flare to the user that the
    # ballometer is offline.
    logging.info('You are offline')

def handle_400(error):
    # Uploading did not work with status code 400 
    # bad request. Let the user somehow know.
    logging.info('Bad request')

def main():
            
    store = ballometer.Store()
    while True:
        while True:
            username, password = get_username_password()
            token = get_jwt_token(username, password)
            if token == '':
                # 80 percent of all problems solve themselves
                time.sleep(10)
            else:
                break

        while True:
            points = store.get_raw_points(start=store.uploaded_until, limit=50)

            if len(points) == 0:
                # no data to upload
                time.sleep(1)
                continue
            
            try:
                r = requests.post(ballometer_url + '/upload/' + username, 
                                json=points,
                                headers={'Authorization': 'Bearer ' + token},
                                timeout=15)
            except requests.exceptions.ConnectTimeout:
                handle_offline()
                time.sleep(10)
                continue
            except requests.exceptions.ConnectionError:
                handle_offline()
                time.sleep(10)
                continue
                
            if r.status_code == 403:
                # Forbidden
                # probably the token has expired
                logging.info('Forbidden, probably the token has expired')
                break
            
            if r.status_code == 200:
                store.uploaded_until = points[-1]['time']
            
            if r.status_code == 400:
                # Bad request
                handle_400(r.text)
            
            if time.time() - store.uploaded_until < 5:
                time.sleep(1)

while True:
    try:
        main()
    except:
        print('houpsi...')
    time.sleep(10)
