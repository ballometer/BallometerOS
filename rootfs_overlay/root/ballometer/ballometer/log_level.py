import json

def get_log_level():
    log_level = 'WARNING'

    try:
        # this file should look like
        # {
        #     "log_level": "WARNING"
        # }
        with open('/data/log_level.json') as f:
            json_level = json.load(f)['log_level']
            if json_level in ['DEBUG', 'INFO', 'WARNING', 'ERROR']:
                log_level = json_level
            
    except json.decoder.JSONDecodeError as e:
        pass
    except FileNotFoundError as e:
        pass
    except KeyError as e:
        pass

    return log_level
