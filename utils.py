import time

def now_ms():
    return int(time.time() * 1000)

class MovingAverage:
    def __init__(self, n=20):
        self.n = n
        self.buf = []
    def push(self, x):
        self.buf.append(x)
        if len(self.buf) > self.n:
            self.buf.pop(0)
    def avg(self):
        return sum(self.buf)/len(self.buf) if self.buf else 0
