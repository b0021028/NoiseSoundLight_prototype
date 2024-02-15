import numpy as np
from warnings import warn
import sounddevice as sd

SINHA = (np.sin(2 * np.pi * 440 * np.linspace(0, 0.25, 4000, endpoint=False)), 16000)


class USBSoundInput:

    dtype = np.int32

    def __init__(self, callbackfunc=None, waitfunc=None, device_port=None):
        if device_port is None:
            warn(
                "deviceport is None :\n device_port choice [input,output] list(int,int) or int\n"
                + f"===Number===\n{sd.query_devices()}\n======\n"
                + f"selected default {sd.default.device}",
                RuntimeWarning,
            )
            device_port = sd.default.device


        self.set_device_port(device_port)

        if callable(waitfunc):
            self.waitfunc = waitfunc
        else:
            self.waitfunc = input

        if callable(callbackfunc):
            self.callback = callbackfunc
        else:
            self.callback = self.callback
            warn(
                "! use default callback\n",
                RuntimeWarning,
            )

    def set_device_port(self, device_port):
        self.device_port = device_port  # [1, 7]  # [1, 5]
        sd.default.device = device_port

    def _callback(self, indata, frames, time, status):
        outdata = np.nan_to_num(indata)
        self.callback(outdata)
        del outdata

    def callback(self, wave: np.ndarray):
        pass

    def rec(self, *args, **kwargs):
        sd.InputStream(
            channels=1,
            dtype=self.dtype,
            callback=self._callback,
        ).start()
        return self
