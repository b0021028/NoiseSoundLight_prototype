from io_output import IROutput
from storage import IRStorage


class Output:
    """アウトプット用class 主に赤外線の発射ができる"""

    def __init__(self):
        self.o = IROutput()
        self.s = IRStorage()

    def output(self, key):
        l = self.s.get(key)
        self.o(20, l)
        print(key, l is not None)
