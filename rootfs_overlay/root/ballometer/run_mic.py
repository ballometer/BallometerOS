import ballometer
import time
import audioop
import logging


logging.basicConfig(
    filename='/var/log/run_mic.log',
    filemode='a',
    format='%(asctime)s %(levelname)s Line %(lineno)d %(message)s',
    level=ballometer.get_log_level()
)
 
logging.info('Starting run_mic...')

def main():
    mic = ballometer.Mic()
    store = ballometer.Store()

    while True:
        try:
            store.save(key='mic_sound_level_1s', value=mic.sound_level_1s)
        except audioop.error:
            logging.info('audioop error')
            time.sleep(1.0)
            

try:
    main()
except:
    logging.exception('')
