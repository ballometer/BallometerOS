import alsaaudio
import audioop
import time


class Mic:
    def __init__(self):
        self._inp = alsaaudio.PCM(
            alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

    @property
    def sound_level(self):
        success = False
        while not success:
            success, data = self._inp.read()
        return float(audioop.rms(data, 2))
    
    @property
    def sound_level_1s(self):
        result = 0.0
        t_start = time.time()
        while time.time() < t_start + 1.0:
            result += self.sound_level
        return result
