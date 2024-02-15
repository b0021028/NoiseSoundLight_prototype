import sounddevice as sd
import numpy as np
import sys
import time
import subprocess

CHANNELS = 1
RATE = 48000
CHUNK =2**10

AS_NEXT = b'''
tell application "Keynote"
    activate
    show next
end tell
'''

class SnappingDetector(object):

    def __init__(self):
        self.x = np.fft.fftfreq(CHUNK, 1.0/RATE)[:int(CHUNK/2)]

        self.preDetect = -1
        self.lastMeans = [0]
        self.keynote = KeynoteControl()

    def start(self):
        self.stream = sd.InputStream(
            dtype=np.int16,
            channels=CHANNELS,
            samplerate=RATE,
            #blocksize=CHUNK,
            callback=self.callback)
        print ("Starting detection...")
        self.stream.start()

    def callback(self, in_data:np.ndarray, frame_count, time_info, status):
        result = np.fft.fft(in_data)
        self.y = np.abs(result)[:int(CHUNK/2)]
        mean = np.mean(self.y)
        var = np.var(self.y)
        meansMean = np.mean(self.lastMeans)
        freqMean = np.mean(self.x * self.y) / mean

        if self.preDetect == -1:
            if 8000 < freqMean and freqMean < 12000 and 10.0*meansMean < mean and 10000 < mean and 200000000 < var:
                self.preDetect = mean
                self.preDetectTime = time.time()
        elif self.preDetectTime + 0.2 < time.time():
            if mean < self.preDetect:
                print('Patchin!')
                self.keynote.next()
            self.preDetect = -1

        if 10 <= len(self.lastMeans):
            self.lastMeans.pop(0)
        self.lastMeans.append(mean)


class KeynoteControl(object):
    def __init__(self):
        return

    def next(self):
        osa = subprocess.Popen('osascript', stdin = subprocess.PIPE)
        osa.stdin.write(AS_NEXT)
        osa.stdin.close()

if __name__ == '__main__':
    a = SnappingDetector()
    a.start()

    inputStr = ""
    while inputStr == "":
        inputStr = input()