import queue, sounddevice as sd, numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

IN_NAME  = os.getenv('INPUT_DEVICE_NAME') or None
OUT_NAME = os.getenv('OUTPUT_DEVICE_NAME') or None

class MicStream:
    def __init__(self, samplerate=16000, blocksize=0, channels=1):
        self.q = queue.Queue()
        self.sr = samplerate
        self.channels = channels
        self.blocksize = blocksize
        self.stream = None

    def _cb(self, indata, frames, time, status):
        if status: print("[mic] status:", status)
        mono = indata[:, 0] if indata.ndim > 1 else indata
        self.q.put(mono.copy())

    def start(self):
        self.stream = sd.InputStream(
            samplerate=self.sr, channels=self.channels,
            dtype='int16', blocksize=self.blocksize,
            callback=self._cb, device=IN_NAME)
        self.stream.start()
        return self

    def read(self, n_samples):
        # read from queue until >= n_samples
        chunks = []
        got = 0
        while got < n_samples:
            data = self.q.get()
            chunks.append(data)
            got += len(data)
        return np.concatenate(chunks)

    def stop(self):
        if self.stream: self.stream.stop(); self.stream.close()

class Speaker:
    def __init__(self, samplerate=24000, channels=1):
        self.sr = samplerate
        self.channels = channels
    def play(self, samples):
        sd.play(samples, self.sr, device=OUT_NAME, blocking=True)
