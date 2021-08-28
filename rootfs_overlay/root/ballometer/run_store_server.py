import uvicorn
import fastapi
import ballometer
from fastapi.middleware.cors import CORSMiddleware
import time


app = fastapi.FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)
store = ballometer.Store()


@app.get('/now')
def get_now():
    '''
        Returns the last measurement of altitude, speed,
        heading, climb, longitude, and latitude. The
        timestamp indicated when the request was processed.
        The field 'recording' shows if the ballometer
        was recording at the time of the request.
        {  
            'altitude': 1464.343,
            'speed': 8.6,
            'heading': 234, 
            'climb': 1.6,
            'longitude': 8.43490,
            'latitude': 43.4309
            'time': 1608397940.45,
            'recording': True
        }
    '''
    result = {}

    point = store.get_saved()

    ui_store_mapping = {
        'altitude': 'vario_altitude',
        'speed': 'gps_speed',
        'heading': 'gps_heading', 
        'climb': 'vario_speed',
        'longitude': 'gps_longitude',
        'latitude': 'gps_latitude'
    }

    for key in ui_store_mapping:
        try:
            result[key] = point[ui_store_mapping[key]]['value']
        except KeyError:
            result[key] = None

    result['time'] = time.time()
    
    result['recording'] = store.recording

    return result

@app.get('/points')
def get_points(flightId: int = None):
    '''
    Returns all the measurements that were stored using linear 
    interpolation. Interval ist 1000 ms up to one hour recording
    and increases then to keep maximal number of points at 3600.
    If flighId is None, returns data for the latest flight.
    {
        'altitude': [918.8838187009885, 919.222839137572, ...], 
        'speed': [12.3, 13.4, ...],
        'climb': [0.5880960494320139, 0.5206506714967045, ...], 
        'longitude': [8.43490, 8.43491, ...], 
        'latitude': [43.64543, 43.645431, ...], 
        'time': [1608369593.0, 1608369594.0, ...]
    }
    '''
    result = {}

    ui_store_mapping = {
        'altitude': 'vario_altitude',
        'speed': 'gps_speed',
        'heading': 'gps_heading', 
        'climb': 'vario_speed',
        'longitude': 'gps_longitude',
        'latitude': 'gps_latitude',
        'time': 'time'
    }

    for key in ui_store_mapping:
        result[key] = []

    points = store.get_history(flight_id=flightId)

    for point in points:
        for key in ui_store_mapping:
            try:
                result[key].append(point[ui_store_mapping[key]])
            except KeyError:
                result[key].append(None)

    return result


@app.get('/listFlights')
def list_flights():
    result = []

    for flight_id in range(store.flight_id + 1):
        start = store.start_time(flight_id)
        if start != 0.0:
            result.append({
                'flight_id': flight_id,
                'start': start
            })

    return result


@app.get('/', response_class=fastapi.responses.HTMLResponse)
def root():
    return '<p>Hello from store. <a href="docs">Docs</a>.</p>'


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, root_path='/store')
