import shutil
import subprocess
import tempfile
import wave
from pathlib import Path

import numpy as np


class TextToSpeechService:
    def __init__(self) -> None:
        self._engine = shutil.which("espeak") or shutil.which("espeak-ng")

    def long_form_synthesize(self, text: str):
        if not self._engine:
            print("TTS engine not found. Install espeak/espeak-ng for audio output.")
            return 16000, np.zeros(1, dtype=np.float32)

        with tempfile.TemporaryDirectory() as tmp_dir:
            wav_path = Path(tmp_dir) / "tts.wav"
            cmd = [self._engine, "-w", str(wav_path), text]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            with wave.open(str(wav_path), "rb") as wf:
                sample_rate = wf.getframerate()
                frames = wf.readframes(wf.getnframes())
                audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

        return sample_rate, audio