###############################################################################################
#     This script is just an experimental prototype, and not a core part of the examples.     #
###############################################################################################
import warnings
from audiomentations import Compose, AddGaussianNoise  # type: ignore
from audiomentations import PitchShift, TimeStretch  # type: ignore
import librosa  # type: ignore
import numpy as np
from examples.audio.models.aec_inference import AudioTagging, labels  # type: ignore

warnings.filterwarnings("ignore")


def get_audio_tagging_result(clipwise_output, top_k=10):
    """Visualization of audio tagging result.
    Args:
      clipwise_output: (classes_num,)
        output softmax distribution across all classes
      top_k: int
        number of top predictions to print
    """
    sorted_indexes = np.argsort(clipwise_output)[::-1]

    # Print audio tagging top probabilities
    for k in range(top_k):
        print(f'{np.array(labels)[sorted_indexes[k]]}: '
              f'{clipwise_output[sorted_indexes[k]]:.3f}')


if __name__ == "__main__":
    DEVICE = 'cpu'
    audio_path = '../acoustic_event_samples/test_aec_audio_0.wav'
    (audio, _) = librosa.core.load(audio_path, sr=32000, mono=True)
    audio = audio[None, :]  # (batch_size, segment_samples)

    # source input
    print('------ Audio tagging Source Input------')
    at = AudioTagging(checkpoint_path=None, device=DEVICE)
    (clipwise_output, embedding) = at.inference(audio)
    get_audio_tagging_result(np.squeeze(clipwise_output))

    # followup inputs
    augment = Compose([
        AddGaussianNoise(min_amplitude=0.001, max_amplitude=0.01, p=0.7),
        TimeStretch(p=0.6),
        PitchShift(min_semitones=-1, max_semitones=+1, p=0.7),
    ], shuffle=True)
    N_AUG = 5
    audio = audio.reshape((-1,))
    for i in range(N_AUG):
        print(f'\n------ Audio tagging Follow up Input: {i+1} ------')
        aug_audio = augment(audio, 32000).reshape((1, -1))
        (clipwise_output_followup, embedding_followup) = at.inference(aug_audio)
        get_audio_tagging_result(np.squeeze(clipwise_output_followup))
