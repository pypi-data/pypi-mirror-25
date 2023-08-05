import threading

class AtomicCount:
    """ An atomic, thread-safe counting iterator """
    def __init__(self,start=0,step=1):
        self.index = 0
        self.start = start
        self.step = step
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            value = self.start + self.index * self.step
            self.index += 1
        return value

