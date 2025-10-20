import asyncio, numpy as np
from dotenv import load_dotenv
from audio_io import MicStream, Speaker
from asr_whisper import ASR
from translator import translate
from tts_edge import tts_np_float

load_dotenv()

SR_IN = 16000
SR_OUT = 24000

async def main():
    mic = MicStream(samplerate=SR_IN).start()
    spk = Speaker(samplerate=SR_OUT)
    asr = ASR(sr=SR_IN)

    print("▶ Ready. Speak Chinese… (Ctrl+C to quit)\n")
    try:
        while True:
            chunk = mic.read(int(SR_IN*0.2))  # 200ms chunk
            text = asr.feed_and_maybe_decode(chunk)
            if text:
                print("[CN]", text)
                en = await translate(text)
                print("[EN]", en)
                if en:
                    samples = await tts_np_float(en, target_sr=SR_OUT)
                    spk.play(samples)
    except KeyboardInterrupt:
        pass
    finally:
        mic.stop()

if __name__ == '__main__':
    asyncio.run(main())
