from inputlayer import SoundValidation
from outputlayer import Output
from storage import FunctionStorage
import time

class Core:
    def __init__(self):
        self.o = Output()
        self.funcs = FunctionStorage()
        self.sound = SoundValidation(self.output)
        pass

    def main(self):
        self.sound.start()
        input()

    def output(self, ct):
        for outputname in self.funcs.get(ct):
            self.o.output(outputname)
            time.sleep(0.0000000001)


if __name__ == "__main__":
    print("Setup ...")
    app = Core()
    print("do >>\n.", end="\r")
    app.main()
