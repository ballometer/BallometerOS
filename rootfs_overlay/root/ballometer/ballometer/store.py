import influxdb
import redis
import time
import requests
import json
import datetime
import dateutil
import calendar


class Store:
    def __init__(self):
        '''
        This constructor is blocking until both influxdb
        and redis respond to ping. This is useful during system
        startup. When the constructor returns, the storage system
        is ready to use.
        '''


        self._influx = influxdb.InfluxDBClient()
        self._redis = redis.Redis(decode_responses=True)

        while True:
            try:
                self._influx.ping()
                self._redis.ping()
                break
            except requests.exceptions.ConnectionError:
                print('InfluxDB is not ready')
                time.sleep(5)
            except redis.exceptions.ConnectionError:
                print('Redis is not ready')
                time.sleep(5)

        self._db_name = 'ballometer'
        if self._influx.switch_database(self._db_name) is None:
            self._influx.create_database(self._db_name)

        if self._redis.get('flight_id') is None:
            # Volatile redis key has not been set yet.
            # Get it from influxdb.
            flight_id = self._get_max_flight_id()
            self._set_volatile_float('flight_id', float(flight_id))

        if self._redis.get('qnh') is None:
            # Volatile redis key has not been set yet.
            # Get it from influxdb.
            qnh = self._get_last_qnh()
            self._set_volatile_float('qnh', float(qnh))
            
        if self._redis.get('uploaded_until') is None:
            # Volatile redis key has not been set yet.
            # Get it from influxdb.
            uploaded_until = self._get_last_uploaded_until()
            self._set_volatile_float('uploaded_until', float(uploaded_until))

    def clock_was_synchronized(self):
        return time.time() > 1601116701.0

    def save(self, key='key-name', value=1.0, unixtime=None):
        '''
        Stores data permanently in influxdb if the system clock has been
        synchronized (and is not at 1970 any more) and recording has
        been turned on.
        '''
        if unixtime is None:
            unixtime = time.time()

        serialized = json.dumps({'value': value, 'unixtime': unixtime})
        redis_key = f'save:{key}'
        self._redis.publish(redis_key, serialized)
        self._redis.set(redis_key, serialized)
        self._redis.sadd('save', key)

        if not self.clock_was_synchronized():
            # The system time is not synchronized yet
            # and is probably still at the default value
            # in year 1970. Skip writing to influxdb.
            return

        if (not self.recording) and (key != 'qnh'):
            # Recording has not been turned on (yet)
            # by the user. Skip writing to influxdb.
            return

        self._influx.write_points([
            {
                'measurement': 'ballometer',
                'fields': {
                    key: float(value)
                },
                'time': datetime.datetime.fromtimestamp(unixtime).isoformat(),
                'tags': {
                    'flight_id': str(self.flight_id)
                }
            }
        ])
        
    def multi_save(self, keys=['key-name'], values=[1.0], unixtime=None):
        '''
        Stores data permanently in influxdb if the system clock has been
        synchronized (and is not at 1970 any more) and recording has
        been turned on.
        '''
        if unixtime is None:
            unixtime = time.time()

        for key, value in zip(keys, values):
            serialized = json.dumps({'value': value, 'unixtime': unixtime})
            redis_key = f'save:{key}'
            self._redis.publish(redis_key, serialized)
            self._redis.set(redis_key, serialized)
            self._redis.sadd('save', key)

        if not self.clock_was_synchronized():
            # The system time is not synchronized yet
            # and is probably still at the default value
            # in year 1970. Skip writing to influxdb.
            return

        if not self.recording:
            # Recording has not been turned on (yet)
            # by the user. Skip writing to influxdb.
            return

        fields = {key: float(value) for key, value in zip(keys, values)}
        
        self._influx.write_points([
            {
                'measurement': 'ballometer',
                'fields': fields,
                'time': datetime.datetime.fromtimestamp(unixtime).isoformat(),
                'tags': {
                    'flight_id': str(self.flight_id)
                }
            }
        ])

    def get_saved(self):
        '''
        Returns for all the keys the last value that was
        saved in the format
        {
            'bmp_pressure': {
                'value': 98443.0,
                'unixtime': 123456.0
            },
            'sht_temperature': {
                'value': 302.1,
                'unixtime': 123456.0
            },
            ...
        }
        '''
        return {
            key: json.loads(self._redis.get(f'save:{key}'))
            for key in self._redis.smembers('save')
        }

    def get_history(self, flight_id=None):
        '''
        Returns all the measurements that were stored using linear 
        interpolation. Interval ist 1000 ms up to one hour recording
        and increases then to keep maximal number of points at 3600.
        If fligh_id is None, returns data for the latest flight.
        [
            {'time': 1605124158.0, 'sht_temperature': 302.1, ...},
            {'time': 1605124159.0, 'sht_temperature': 300.4, ...},
            ...
        ]
        '''
        res = []

        if flight_id is None:
            my_flight_id = self.flight_id
        else:
            my_flight_id = flight_id

        start = self.start_time(my_flight_id)
        stop = self.stop_time(my_flight_id)

        # Query at most 3600 points. If recording is shorter than
        # 1 hour, the intervall is 1000 ms, else it gets longer.
        # Examples: 
        # 5 minutes recording -> 1000 ms interval
        # 1 hour recording -> 1000 ms interval
        # 2 hours recording -> 2000 ms interval
        interval_ms = max(1000, int((stop - start) / 3600 / 1e-3))
        
        query_str = 'SELECT mean(*)'
        query_str += ' FROM ballometer'
        query_str += ' WHERE flight_id = \'' + str(my_flight_id) + '\''
        query_str += ' AND time >= \'' + self._unixtime_to_str(start) + '\''
        query_str += ' AND time <= \'' + self._unixtime_to_str(stop) + '\''
        query_str += ' GROUP BY time(' + str(interval_ms) + 'ms) fill(linear)'

        q = self._influx.query(query_str)
        # list(q) ->
        # [[{'time': '2020-11-11T19:49:18Z', 'mean_field_1': None, ...},
        # ...
        # ]]

        try:
            data = list(q)[0]
        except IndexError:
            data = []

        res = [self._remove_mean(self._cast_time(point)) for point in data]
        return res
    
    def get_raw_points(self, start, limit):
        '''
        start: get point from but not including start unix timestamp
        limit: maximum number of points to get with distinct timestamps
        returns: 
        [
            {
                'time': 1605120075.645165,
                'sht_temperature': 304.5,
                'flight_id': 1
            },
            {
                'time': 1605120077.493095,
                'sht_humidity': 43.3,
                'flight_id': 1
            },
            ...
        ]
        '''
        
        result = []
            
        query_str = 'SELECT *'
        query_str += ' FROM ballometer'
        query_str += ' WHERE time > \'' + self._unixtime_to_str(start) + '\''
        query_str += ' LIMIT ' + str(int(limit))
        
        q = self._influx.query(query_str)

        try:
            points = list(q)[0]
        except IndexError:
            points = []
        
        points = [{key: point[key] for key in point if point[key]} for point in points]
        
        for point in points:
            point['time'] = self._str_to_unixtime(point['time'])
            
        # some points have multiple keys with the same timestamp, for example
        # {'time': 1605197178.116631, 'bmp_pressure': 97070.8, 'flight_id': '38', 
        # 'vario_altitude': 432.1882592305743, 'vario_speed': -0.0012395201852855582}
        #
        # split them into individual points
        
        for point in points:
            time = point['time']
            flight_id = point['flight_id']
            result += [{
                'time': time, 'flight_id': flight_id, key: point[key]
            } for key in point if key != 'time' and key != 'flight_id']
            
        return result

    def _str_to_unixtime(self, s):
        '''
        str_to_unixtime('2020-11-11T18:41:15.645165Z') ->1605120075.645165
        '''
        d = dateutil.parser.parse(s)
        return calendar.timegm(d.timetuple()) + d.microsecond * 1e-6

    def _unixtime_to_str(self, t):
        '''
        unixtime_to_str(1605120075.645165) -> '2020-11-11T18:41:15.645165Z'
        '''
        d = datetime.datetime.utcfromtimestamp(t)
        return d.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    
    def start_time(self, flight_id):
        start = 0.0
        
        query_str = 'SELECT * FROM ballometer'
        query_str += ' WHERE flight_id = \'' + str(int(flight_id)) + '\''
        query_str += ' LIMIT 1'
        q = self._influx.query(query_str)
        try:
            t = [self._str_to_unixtime(point['time']) for point in list(q)[0]]
            start = min(t)
        except IndexError:
            pass
        
        return start
    
    
    def stop_time(self, flight_id):
        stop = 0.0
        
        query_str = 'SELECT * FROM ballometer'
        query_str += ' WHERE flight_id = \'' + str(int(flight_id)) + '\''
        query_str += ' ORDER BY time DESC LIMIT 1'
        q = self._influx.query(query_str)
        try:
            t = [self._str_to_unixtime(point['time']) for point in list(q)[0]]
            stop = max(t)
        except IndexError:
            pass
        
        return stop
        

    def _remove_mean(self, point):
        '''
        p = {'time': '...', 'mean_field_1': None, 'mean_field_2': None}
        remove_mean(p) -> {'time': '...', 'field_1': None, 'field_2': None}
        '''
        return {key.replace('mean_', ''): point[key] for key in point}

    def _cast_time(self, point):
        '''
        p = {'time': '2020-11-11T19:49:18Z', 'mean_field_1': ...}
        cast_time(p) -> {'time': 1605124158.0, 'mean_field_1': ...}
        '''
        res = dict(point)
        res['time'] = self._str_to_unixtime(point['time'])
        return res

    def _get_volatile_float(self, key='key-name'):
        value = self._redis.get(key)
        if value is None:
            return 0.0
        return float(value)

    def _set_volatile_float(self, key='key-name', value=1.0):
        self._redis.set(key, str(float(value)))

    def _get_max_flight_id(self) -> int:
        q = self._influx.query('SHOW TAG VALUES WITH KEY = "flight_id"')
        # list(q.get_points()) is [{'key': 'flight_id', 'value': '1'}, ...]
        values = [int(point['value']) for point in q.get_points()]
        if len(values) == 0:
            return 0
        return max(values)

    def _get_last_qnh(self) -> int:
        q = self._influx.query(
            'SELECT "qnh" FROM "ballometer" ORDER BY DESC LIMIT 1')
        # list(q.get_points()) is
        # [{'time': '2020-10-03T18:10:00Z', 'qnh': 1018.0}]
        values = [int(point['qnh']) for point in q.get_points()]
        if len(values) == 0:
            return 1013
        return values[0]
    
    def _get_last_uploaded_until(self) -> float:
        q = self._influx.query(
            'SELECT "uploaded_until" FROM "upload" ORDER BY DESC LIMIT 1')
        # list(q.get_points()) is
        # [{'time': '2020-10-03T18:10:00Z', 'uploaded_until': 1605197196.978443}]
        values = [float(point['uploaded_until']) for point in q.get_points()]
        if len(values) == 0:
            return 0.0
        return values[0]

    @property
    def recording(self) -> bool:
        return bool(self._get_volatile_float('recording'))

    @recording.setter
    def recording(self, value: bool):
        if value:
            self.save('qnh', float(self.qnh))
        self._set_volatile_float('recording', float(value))

    @property
    def flight_id(self) -> int:
        return int(self._get_volatile_float('flight_id'))

    @flight_id.setter
    def flight_id(self, value: int):
        self._set_volatile_float('flight_id', float(value))

    @property
    def qnh(self) -> int:
        return int(self._get_volatile_float('qnh'))

    @qnh.setter
    def qnh(self, value: int):
        if self.recording:
            self.save('qnh', float(value))
        self._set_volatile_float('qnh', float(value))
        
    @property
    def uploaded_until(self) -> float:
        return float(self._get_volatile_float('uploaded_until'))
    
    @uploaded_until.setter
    def uploaded_until(self, value: float):
        self._influx.write_points([
            {
                'measurement': 'upload',
                'fields': {
                    'uploaded_until': float(value)
                }
            }
        ])
        self._set_volatile_float('uploaded_until', float(value))

    @property
    def qnh_station_id(self) -> str:
        try:
            with open('/data/qnh_station_id.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.qnh_station_id = 'LSZH'
            return 'LSZH'

    @qnh_station_id.setter
    def qnh_station_id(self, value):
        with open('/data/qnh_station_id.json', 'w') as f:
            json.dump(value, f)
