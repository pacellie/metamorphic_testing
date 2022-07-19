import soundfile  # type: ignore
from pathlib import Path
import os


def read_audio_from_idx(idx):
    audio, sample_rate = soundfile.read(
        file=f"tests/speech_samples/test_audio_{idx}.wav",
        always_2d=True,
        dtype='float32',
    )
    return sample_rate, audio.T


def write_audio(audio, sr, file_name, dir_path):
    if not dir_path:
        return
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    soundfile.write(os.path.join(dir_path, file_name), audio, sr)
