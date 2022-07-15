import numpy
from audiomentations import Compose, AddGaussianNoise  # type: ignore
from audiomentations import PitchShift, AddBackgroundNoise  # type: ignore
import soundfile  # type: ignore
from typing import Union, List
from pathlib import Path
from scipy.io.wavfile import read
import torch
import os

import pytest
from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    randomized,
    randint,
    approximately,
    equality
)

# register the metamorphic testcases for speech recognition
# with_gaussian_noise = metamorphic('with_gaussian_noise', relation=equality)
# with_background_noise = metamorphic('with_background_noise', relation=equality)
with_altered_pitch = metamorphic('with_altered_pitch', relation=equality)


# with_combined_effect = metamorphic('with_combined_effect', relation=equality)


# define and register the audio transformations
# transformation to add Gaussian noise:
# @transformation(with_gaussian_noise)
# @randomized('min_amplitude', 0.0001)
# @randomized('max_amplitude', 0.001)
# @randomized('p', 1.)
# def add_gaussian_noise(
#         source_audio: Union[numpy.ndarray, torch.Tensor],
#         min_amplitude: float,
#         max_amplitude: float,
#         p: float
# ):
#     """
#     This transformation adds a random Gaussian noise (within min_amplitude and max_amplitude)
#     to the source_audio with probability p and returns that transformed audio.
#
#     params:
#         source_audio: numpy ndarray of shape (<number of samples>,): the input audio
#         min_amplitude: float: minimum amplitude of the Gaussian noise
#         max_amplitude: float: maximum amplitude of the Gaussian noise
#         p: float: probability of applying the transformation
#
#     returns:
#         numpy ndarray of shape (<number of samples>,) (same shape of input)
#     """
#     transform = AddGaussianNoise(min_amplitude=min_amplitude, max_amplitude=max_amplitude, p=p)
#     if not torch.is_tensor(source_audio):
#         return torch.from_numpy(transform(source_audio, 16000))
#     else:
#         return torch.from_numpy(transform(source_audio.numpy(), 16000))


# transformation to add background noise
# @transformation(with_background_noise)
# @randomized('sounds_path', "../audio_examples/background_noises")
# @randomized('p', 1.)
# def add_background_noise(
#         source_audio: numpy.ndarray,
#         sounds_path: Union[List[Path], List[str], Path, str],
#         p: float
# ):
#     """
#     This transformation adds a random background noise from the sounds_path folder
#     to the source_audio with probability p and returns that transformed audio.
#
#     params:
#         source_audio: numpy ndarray of shape (<number of samples>,): the input audio
#         sounds_path: A path or list of paths to audio file(s) and/or folder(s) with
#             audio files. Can be str or Path instance(s). The audio files given here are
#             supposed to be background noises.
#         p: float: probability of applying the transformation
#
#     returns:
#         numpy ndarray of shape (<number of samples>,) (same shape of input)
#     """
#     transform = AddBackgroundNoise(sounds_path=sounds_path, p=p)
#     return transform(source_audio, 16000)  # 16000 is the sampling rate, but not that important


# transformation to alter pitch
@transformation(with_altered_pitch)
@randomized('min_semitones', -1)
@randomized('max_semitones', 1)
@randomized('p', 1.)
def alter_pitch(
        source_audio: Union[numpy.ndarray, torch.Tensor],
        min_semitones: int,
        max_semitones: int,
        p: float
) -> torch.Tensor:
    """
    This transformation randomly alters the pitch of the source_audio within min_semitones and
    max_semitones with probability p and returns the transformed audio

    params:
        source_audio: numpy ndarray of shape (<number of samples>,): the input audio
        min_semitones: int: lower limit of the pitch alteration. A -ve value implies pitch
            should be lowered from the pitch of the source_audio
        max_semitones: int: upper limit of the pitch alteration
         p: float: probability of applying the transformation

    returns:
        torch tensor of shape (<number of samples>,) (same shape of input)
    """
    transform = PitchShift(min_semitones=min_semitones, max_semitones=max_semitones, p=p)
    if not torch.is_tensor(source_audio):
        return torch.from_numpy(transform(source_audio, 16000))
    else:
        return torch.from_numpy(transform(source_audio.numpy(), 16000))


# now define relations (only for complex relations, as of now equality works). later on


def read_audio(idx):  # util file, not in use currently
    audio, sample_rate = soundfile.read(
        file=f"tests/speech_samples/test_audio_{idx}.wav",
        always_2d=True,
        dtype='float32',
    )
    print(sample_rate)
    print(audio.shape)
    return sample_rate, audio.T


def write_audio(audio, sr, file_name, dir_path):
    if not dir_path:
        return
    Path(dir_path).mkdir(parents=True, exist_ok=True)
    soundfile.write(os.path.join(dir_path, file_name), audio, sr)


class SpeechToText:
    def __init__(
            self,
            repo_or_dir='snakers4/silero-models',
            model_name='silero_stt',
            language='en',  # also available 'de', 'es'
            device=torch.device('cpu')
    ):
        self.device = device
        self.repo = repo_or_dir
        self.model_name = model_name
        self.language = language

        self.model, self.decoder, utils = torch.hub.load(
            repo_or_dir=self.repo,
            model=self.model_name,
            language=self.language,  # also available 'de', 'es'
            device=self.device
        )
        self.read_audio = utils[2]
        self.prepare_input = utils[3]

    def recognize(self, audio: Union[torch.Tensor, numpy.ndarray]):
        # def recognize(self, idx: int):
        # audio = self.read_audio(f"tests/speech_samples/test_audio_1.wav")
        print(audio.shape)
        if audio.ndim == 1:
            audio = audio.reshape(1, -1)
        else:
            assert audio.ndim == 2, f"Input audio must have either 1 or 2 dimension. " \
                                    f"But received {audio.ndim} instead"
            assert audio.shape[0] == 1, f"stereo audio is not supported. " \
                                        f"First dimension must be singleton. " \
                                        f"But received {audio.shape[0]} instead."
        if not torch.is_tensor(audio):
            assert isinstance(audio, numpy.ndarray), "input audio must be of type " \
                                                     "numpy.ndarray or torch.Tensor."
            # print("Converting to tensor")
            audio = torch.from_numpy(audio)

            # print(audio)
            # print(audio.size())
            # print(audio.shape)
            # print(type(audio))

        intermediate = self.model(audio).squeeze(0)
        print(intermediate.shape)
        recognized_text = self.decoder(intermediate.cpu())

        return recognized_text


stt = SpeechToText()
src_audio = stt.read_audio(f"tests/speech_samples/test_audio_1.wav")


# system under test
# Parametrize the input (audio file indices), in this case: [0,4]
@pytest.mark.parametrize('audio', [src_audio])
# Mark this function as the system under test
@system
def test_stt(audio):
    return stt.recognize(audio)
