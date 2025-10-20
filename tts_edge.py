import asyncio
import numpy as np
from pydub import AudioSegment
from io import BytesIO
import edge_tts
from dotenv import load_dotenv
import os

load_dotenv()
VOICE = os.getenv('TTS_VOICE','en-US-JennyNeural')
RATE  = os.getenv('TTS_RATE','+0%')
PITCH = os.getenv('TTS_PITCH','+0Hz')

async def tts_bytes(text: str) -> bytes:
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE, pitch=PITCH)
    buf = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])  # bytes of mp3
    return buf.getvalue()

async def tts_np_float(text: str, target_sr=24000):
    mp3 = await tts_bytes(text)
    seg = AudioSegment.from_file(BytesIO(mp3), format="mp3")
    seg = seg.set_frame_rate(target_sr).set_channels(1)
    samples = np.array(seg.get_array_of_samples()).astype('float32') / (2**15)
    return samples
