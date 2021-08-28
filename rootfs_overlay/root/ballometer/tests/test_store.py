import ballometer


def test_constructor(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    ballometer.Store()


def test_clock_was_synchronized(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    store = ballometer.Store()

    assert store.clock_was_synchronized() is True

    mocker.patch('time.time', return_value=0.0)
    assert store.clock_was_synchronized() is False


def test_save(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    store = ballometer.Store()

    mocker.patch('redis.Redis.publish')
    mocker.patch('redis.Redis.sadd')
    mocker.patch('influxdb.InfluxDBClient.write_points')

    store.save(key='bmp_pressure', value=94034.0)

def test_get_saved(mocker):
    mocker.patch('redis.Redis.ping')
    mocker.patch('influxdb.InfluxDBClient.ping')
    mocker.patch('redis.Redis.get')
    mocker.patch('redis.Redis.set')
    mocker.patch('influxdb.InfluxDBClient.query')
    store = ballometer.Store()
    
    def smembers(self, name):
        if name == 'save':
            return {b'bmp_pressure'}
        else:
            return {}
        
    mocker.patch('redis.Redis.smembers', smembers)
    mocker.patch('redis.Redis.get', return_value='{"value": 94893.0, "unixtime": 123456}')
    assert store.get_saved() == {'bmp_pressure': {'value': 94893.0, 'unixtime': 123456}}
    