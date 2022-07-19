import numpy
from audiomentations import Compose, AddGaussianNoise  # type: ignore
from audiomentations import PitchShift, AddBackgroundNoise  # type: ignore
import soundfile  # type: ignore
from typing import Union, List
from pathlib import Path
import torch
import pytest
import warnings

from models.speech_to_text import SpeechToText
from utils.stt_utils import stt_read_audio
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

warnings.filterwarnings("ignore")

# region test_names
# register the metamorphic testcases for speech recognition
with_gaussian_noise = metamorphic('with_gaussian_noise', relation=equality)
with_background_noise = metamorphic('with_background_noise', relation=equality)
with_altered_pitch = metamorphic('with_altered_pitch', relation=equality)
# with_combined_effect = metamorphic('with_combined_effect', relation=equality)
# endregion


# region custom_transformations

# define and register the audio transformations
# transformation to add Gaussian noise:
@transformation(with_gaussian_noise)
@randomized('min_amplitude', 0.0001)
@randomized('max_amplitude', 0.001)
@randomized('p', 1.)
def add_gaussian_noise(
        source_audio: Union[numpy.ndarray, torch.Tensor],
        min_amplitude: float,
        max_amplitude: float,
        p: float
):
    """
    This transformation adds a random Gaussian noise (within min_amplitude and max_amplitude)
    to the source_audio with probability p and returns that transformed audio.

    params:
        source_audio: numpy ndarray of shape (<number of samples>,): the input audio
        min_amplitude: float: minimum amplitude of the Gaussian noise
        max_amplitude: float: maximum amplitude of the Gaussian noise
        p: float: probability of applying the transformation

    returns:
        numpy ndarray of shape (<number of samples>,) (same shape of input)
    """
    transform = AddGaussianNoise(min_amplitude=min_amplitude, max_amplitude=max_amplitude, p=p)
    if not torch.is_tensor(source_audio):
        return torch.from_numpy(transform(source_audio, 16000))
    else:
        return torch.from_numpy(transform(source_audio.numpy(), 16000))


# transformation to add background noise
@transformation(with_background_noise)
@randomized('sounds_path', "examples/audio/background_noises")
@randomized('p', 1.)
def add_background_noise(
        source_audio: Union[numpy.ndarray, torch.Tensor],
        sounds_path: Union[List[Path], List[str], Path, str],
        p: float
):
    """
    This transformation adds a random background noise from the sounds_path folder
    to the source_audio with probability p and returns that transformed audio.

    params:
        source_audio: numpy ndarray of shape (<number of samples>,): the input audio
        sounds_path: A path or list of paths to audio file(s) and/or folder(s) with
            audio files. Can be str or Path instance(s). The audio files given here are
            supposed to be background noises.
        p: float: probability of applying the transformation

    returns:
        numpy ndarray of shape (<number of samples>,) (same shape of input)
    """
    transform = AddBackgroundNoise(sounds_path=sounds_path, p=p)
    if not torch.is_tensor(source_audio):
        return torch.from_numpy(transform(source_audio, 16000))
    else:
        return torch.from_numpy(transform(source_audio.numpy(), 16000))


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

# endregion


# region custom_relations
# todo:
# endregion


# region model
stt = SpeechToText()
# endregion


# region data_list
src_audios = [stt_read_audio(f"examples/audio/speech_samples/test_audio_{i}.wav") for i in range(1, 3)]
# endregion


# region system under test
# Parametrize the input (audio file indices), in this case: [0,4]
@pytest.mark.parametrize('audio', src_audios)
# Mark this function as the system under test
@system
def test_stt(audio):
    return stt.recognize(audio)
# endregion
