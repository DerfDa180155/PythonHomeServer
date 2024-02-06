import threading
import time

class TestThread(threading.Thread):
    def __init__(self, name, sleepTime=10, debug=False):
        threading.Thread.__init__(self)
        self.name = name
        self.sleepTime = sleepTime
        self.debug = debug
        self.running = True

    def __del__(self):
        print(self.name + " | deleted!")

    def run(self):
        print(self.name + " | started!")
        time.sleep(1)

        while self.running:
            print(self.name + " | running!")
            time.sleep(self.sleepTime)

        print(self.name + " | stopped!")

