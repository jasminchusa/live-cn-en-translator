import numpy as np, webrtcvad
from faster_whisper import WhisperModel
from dotenv import load_dotenv
import os

load_dotenv()
MODEL_NAME = os.getenv('ASR_MODEL', 'base')
BEAM = int(os.getenv('ASR_BEAM', '1'))
DEVICE = os.getenv('ASR_DEVICE', 'auto')
CHUNK_MS = int(os.getenv('CHUNK_MS', '800'))
PAUSE_MS = int(os.getenv('PAUSE_MS', '400'))
VAD_AGGR = int(os.getenv('VAD_AGGRESSIVENESS','2'))

class ASR:
    def __init__(self, sr=16000):
        self.sr = sr
        self.model = WhisperModel(MODEL_NAME, device=DEVICE, compute_type="int8" if DEVICE!="cuda" else "float16")
        self.vad = webrtcvad.Vad(VAD_AGGR)
        self.buf = b""
        self.pause_bytes = int(self.sr * (PAUSE_MS/1000.0))

    def _frames(self, pcm16):
        # yield 20ms frames for VAD
        frame_len = int(self.sr*0.02)
        for i in range(0, len(pcm16), frame_len):
            yield pcm16[i:i+frame_len]

    def feed_and_maybe_decode(self, samples):
        # samples: np.int16 mono
        pcm16 = samples.astype(np.int16).tobytes()
        self.buf += pcm16
        # VAD on the latest chunk
        try:
            voiced = any(self.vad.is_speech(f.tobytes(), self.sr) for f in self._frames(np.frombuffer(pcm16, dtype=np.int16)))
        except Exception:
            voiced = True
        if not voiced:
            # silence chunk: if buffer long enough, finalize a segment
            if len(self.buf)//2 >= self.pause_bytes:
                segment = np.frombuffer(self.buf, dtype=np.int16).astype(np.float32)/32768.0
                self.buf = b""
                if len(segment) > self.sr*0.2:
                    return self._decode(segment)
            return None
        else:
            # keep buffering during speech
            if len(self.buf)//2 >= self.sr*6:  # 6s safety window
                segment = np.frombuffer(self.buf, dtype=np.int16).astype(np.float32)/32768.0
                self.buf = b""
                return self._decode(segment)
            return None

    def _decode(self, float_mono):
        segments, info = self.model.transcribe(float_mono, language='zh', beam_size=BEAM)
        text = ''.join([s.text for s in segments])
        return text.strip()
