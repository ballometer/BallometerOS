import requests
import json

def get_metar(station_id='LSZH'):
    try:
        url = f'https://api.ballometer.io/weather/metar?station_id={station_id}'
        r = requests.get(url, timeout=1.0)
        if r.status_code != 200:
            return {}
        data = json.loads(r.text)
        return {
            'press': float(data['press']),
            'station_id': str(data['station_id']),
            'time': float(data['time']),
        }
    except:  # catch-all because used in menu which needs to stay alive
        return {}

if __name__ == '__main__':
    print(get_metar('LSGG'))
