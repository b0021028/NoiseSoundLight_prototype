import pigpio
import time

class IROutput:
    """アウトプット用class 主に赤外線の発射ができる"""

    def __init__(self):
        self.__work = 0

        self.IR_PIN = 20
        self.kHz = 38.0
        self.GAP_Second = 1
        self.WAVE_WAIT = 0.002
        self.pi = pigpio.pi(show_errors=False)
        if not self.pi.connected:
            raise ConnectionError("Can't connect to the pigpiod deamon")

    def reset(self):
        pass

    def carrier(self, micros):
        """
        Generate carrier square wave.
        """
        wf = []
        cycle = 1000.0 / self.kHz
        cycles = int(round(micros / cycle))
        on_delay = int(round(cycle / 2.0))
        sofar = 0
        for c in range(cycles):
            target = int(round((c + 1) * cycle))
            sofar += on_delay
            off_delay = target - sofar
            sofar += off_delay
            wf.append(pigpio.pulse(1 << self.IR_PIN, 0, on_delay))
            wf.append(pigpio.pulse(0, 1 << self.IR_PIN, off_delay))
        return wf

    _pulse = pigpio.pulse

    def _send(self, code):
        GPIO = self.pi
        try:
            GPIO.set_mode(self.IR_PIN, pigpio.OUTPUT)
            GPIO.wave_add_new()
            emit_time = time.time()
            if not code:
                return

            marks_wid, spaces_wid = {}, {}
            CODE_LEN = len(code)
            wave = [0] * CODE_LEN

            for i, ci in enumerate(code):  # range(CODE_LEN):
                if (i & 1) == 1:  # Space 1,3,... 回目
                    if ci not in spaces_wid:
                        GPIO.wave_add_generic([pigpio.pulse(0, 0, ci)])
                        spaces_wid[ci] = GPIO.wave_create()
                    wave[i] = spaces_wid[ci]
                else:  # Mark 0,2,... 回目
                    if ci not in marks_wid:
                        wf = self.carrier(ci)
                        GPIO.wave_add_generic(wf)
                        marks_wid[ci] = GPIO.wave_create()
                    wave[i] = marks_wid[ci]

            delay = emit_time - time.time()

            if delay > 0.0:
                time.sleep(delay)

            GPIO.wave_chain(wave)
            while GPIO.wave_tx_busy():
                time.sleep(self.WAVE_WAIT)

            emit_time = time.time() + self.GAP_Second

            for i in marks_wid:
                GPIO.wave_delete(marks_wid[i])

            for i in spaces_wid:
                GPIO.wave_delete(spaces_wid[i])

            del marks_wid, spaces_wid

        finally:
            GPIO.write(self.IR_PIN, 0)

    def _work(self):
        """並"行"処理 用の work権"""
        self.__work += 1
        if self.__work == 1:
            return True
        self.__work -= 1
        return False

    def send(self, PIN, code):
        """send output"""
        if self._work():
            self.IR_PIN = PIN
            try:
                self._send(code)
            finally:
                self.__work -= 1

    def __del__(self):
        self.pi.stop()


    __call__ = send
