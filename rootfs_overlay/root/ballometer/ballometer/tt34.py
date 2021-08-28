import RPi.GPIO as GPIO
import time
import numpy as np
import json
from scipy.interpolate import interp1d

def record(N_max, recording_time):
    t = np.zeros(N_max)
    state = np.zeros(N_max)
    
    i = 0
    last_state = 0

    t[i] = time.time()
    state[i] = last_state

    i += 1
    
    while (time.time() - t[0] < recording_time) and (i < N_max):
        if last_state == 0:
            GPIO.wait_for_edge(4, GPIO.FALLING)
            last_state = 1
        else:
            GPIO.wait_for_edge(4, GPIO.RISING)
            last_state = 0

        state[i] = last_state
        t[i] = time.time()

        i += 1

    t -= t[0]

    t = t[0:i]
    state = state[0:i]
    
    return (t, state)

def zoom(t, state, signal_length, minimum_low_dt):
    
    dt = np.diff(t)
    idx_end = np.argmax(dt)
    dt_max = dt[idx_end]
    
    if int(state[idx_end + 1]) == 1:
        raise Exception('state dt max is high')
    
    if dt[idx_end] < minimum_low_dt:
        raise Exception('minimum_low_dt not reached')
    
    if t[idx_end] - signal_length < 0.0:
        raise Exception('signal_length not reached')
        
    idx_zoom = (t[idx_end] - signal_length <= t) & (t <= t[idx_end])
    
    t_zoom = t[idx_zoom]
    state_zoom = state[idx_zoom]
    
    return (t_zoom, state_zoom, dt_max)

def get_start_index(t_data, data, period):
    i = 0
    
    # get to the start of the the oscillations
    while True:
        next_dt = t_data[i + 2] - t_data[i]
        if (0.8 * 2 * period < next_dt) and (next_dt < 1.2 * 2 * period):
            break
        else:
            i += 1
            
    # get to the end of the oscillations
    while True:
        next_dt = t_data[i + 2] - t_data[i]
        if (0.8 * 2 * period < next_dt) and (next_dt < 1.2 * 2 * period):
            i += 1
        else:
            break
            
    return i

def interpolate_data(t_zoom, state_zoom, period):
    t_data = np.arange(t_zoom[0] + period / 2, t_zoom[-1], period)
    data = interp1d(t_zoom, state_zoom, kind='next')(t_data)
    
    return (t_data, data)

def parse_digit(data, shift):
    result = 0.0
       
    result += 1.0 * ((int(data[0 + shift]) << 0) + (int(data[1 + shift]) << 1) + (int(data[2 + shift]) << 2) + (int(data[3 + shift]) << 3))

    return result

def parse(data):
    
    shift = 22
    
    temperature = 0
    address = 0
    
    if len(data) < shift + 4 + 2 + 4 + 4 + 4:
        raise Exception('data length is too short')

    temperature += 0.1 * parse_digit(data, shift)
    temperature += 1.0 * parse_digit(data, shift + 4)
    temperature += 10.0 * parse_digit(data, shift + 4 + 2 + 4)
    temperature += 100.0 * parse_digit(data, shift + 4 + 2 + 4 + 4)
    
    if temperature > 155:
        raise Exception('temperature larger than 155 deg C')
        
    s = ''
    for x in data:
        s += str(int(x))
    
    address = int(s[1:shift], 2)
    
    return (temperature, address)

def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)
    

def get():
    try:
        N_max = 10000

        recording_time = 6 # s

        t, state = record(N_max, recording_time)

        minimum_low_dt = 10 * 1e-3 # s
        period = 1042 * 1e-6 # s
        signal_length = 60 * period # s
        t_zoom, state_zoom, dt_max = zoom(t, state, signal_length, minimum_low_dt)
        
        start_index = get_start_index(t_zoom, state_zoom, period)
        t_zoom_started = t_zoom[start_index:]
        state_zoom_started = state_zoom[start_index:]
        t_data, data = interpolate_data(t_zoom_started, state_zoom_started, period)
        data_inverted = 1 - data
        
        return parse(data_inverted)
    except Exception as e:
        print(format(e))
        return (0, 0)
