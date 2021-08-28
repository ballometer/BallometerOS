import time
import ballometer


while True:
    try:
        ballometer.upload.run()
    except:
        print('houpsi...')
    time.sleep(10)
