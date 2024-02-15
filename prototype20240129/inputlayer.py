import numpy as np
from io_input import USBSoundInput

MAXINT = 2**31 - 1


class SoundValidation:
    def catch_sound(self, ct):
        ...

    wave: np.ndarray

    def __init__(self, catch_sound=None):
        # 閾値
        self.threshold = 500000000
        self.min_threshold = 0  # self.threshold // 100
        self.max_threshold = self.threshold * 5

        # 反応時間
        self.heardtime = 20  # 反応後の検知時間 (音の持続性)
        self.heard = 0
        # 反応回数
        self.max_sound_doc = 0
        self.max_sound_sec = 0
        # 検出音時間
        self.sound_secthres_hold = 10
        self._keta = len(f"{self.max_threshold}")

        if callable(catch_sound):
            self.catch_sound = catch_sound
        else:
            self.catch_sound = lambda self: None

    def callback(self, wave: np.ndarray):
        wave = np.abs(np.nan_to_num(wave).astype(np.int32)).clip(
            self.min_threshold, MAXINT
        )
        wave = np.abs(np.fft.fft(wave))

        # input()

        value = int((np.mean(wave) + np.max(wave)) / 2)
        flg = False
        if value > self.threshold:
            self.heard = self.heardtime
            self.max_sound_doc += 1
            self.max_sound_sec += 1
        elif self.heard > 0:
            self.heard -= 1
        elif self.max_sound_doc > 0:
            self.max_sound_doc -= 1
            if self.max_sound_doc == 0:
                if self.max_sound_sec <= self.sound_secthres_hold:
                    self._catch_sound()
                    flg = True
                self.max_sound_sec = 0
        if not flg:
            self.no_catch_sound()

    _CATCH_TIME = 100
    no_catch_sound_flag = _CATCH_TIME
    _catch_count = 0
    _do_flg = False

    def _catch_sound(self):
        self._catch_count += 1
        self.no_catch_sound_flag = 0
        print(self._catch_count, end="\r")

    def no_catch_sound(self):
        if self.no_catch_sound_flag < self._CATCH_TIME:
            self.no_catch_sound_flag += 1
            self._do_flg = True
        elif self._do_flg:
            m = self._catch_count
            self._catch_count = 0
            self._do_flg = False
            self.catch_sound(m)

    def start(self):
        device = USBSoundInput(callbackfunc=self.callback)
        device.dtype = np.int32
        device.rec()
