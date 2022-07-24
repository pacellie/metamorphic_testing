import os
from pathlib import Path
import soundfile  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import uuid
import torch


def save_spectrogram_plot(audio: np.ndarray, path: str, sampling_rate: int = 16000) -> None:
    """
    Saves the spectrogram (time-frequency domain) plot of an audio as an image

    Parameters
    ----------
    audio: np.ndarray
        audio for which spectrogram needs to be calculated. It needs to be a mono audio
        as a numpy ndarray of shape (N,) where N is the total number of samples of the
        audio.

    path: str
        full path of the spectrogram file that needs to be saved

    sampling_rate: int
        sampling rate of the speech audio. It refers to number of samples to represent
        just one second of audio.

    See Also
    --------
    save_waveform_plot: saves the waveform plot of an audio as an image
    save_audio: save the waveform audio as audio

    """
    plt.figure()
    plt.axis("off")
    plt.tight_layout()
    plt.specgram(audio, Fs=sampling_rate)
    plt.savefig(path, bbox_inches='tight')


def save_waveform_plot(audio: np.ndarray, path: str, sampling_rate: int = 16000) -> None:
    """
    Saves the waveform (time-domain) plot of an audio as an image

    Parameters
    ----------
    audio: np.ndarray
        audio for which spectrogram needs to be calculated. It needs to be a mono audio
        as a numpy ndarray of shape (N,) where N is the total number of samples of the
        audio.

    path: str
        full path of the spectrogram file that needs to be saved

    sampling_rate: int
        sampling rate of the speech audio. It refers to number of samples to represent
        just one second of audio.

    See Also
    --------
    save_spectrogram_plot: Saves the spectrogram plot of an audio as an image
    save_audio: save the waveform audio as audio

    """
    plt.figure()
    time = np.linspace(0, len(audio) / sampling_rate, num=len(audio))
    plt.axis("off")
    plt.tight_layout()
    plt.plot(time, audio, color="green")
    plt.savefig(path, bbox_inches='tight')


def save_audio(audio: np.ndarray, path: str, sampling_rate: int = 16000) -> None:
    """
    Saves an audio as a .wav file

    Parameters
    ----------
    audio: np.ndarray
        audio for which spectrogram needs to be calculated. It needs to be a mono audio
        as a numpy ndarray of shape (N,) where N is the total number of samples of the
        audio.

    path: str
        full path of the spectrogram file that needs to be saved

    sampling_rate: int
        sampling rate of the speech audio. It refers to number of samples to represent
        just one second of audio.

    See Also
    --------
    save_spectrogram_plot: Saves the spectrogram plot of an audio as an image
    save_waveform_plot: saves the waveform plot of an audio as an image

    """
    soundfile.write(path, audio, sampling_rate)


def audio_input_visualizer(audio: torch.Tensor) -> str:
    """
    Log and Visualize audio in the html test report

    Parameters
    ----------
    audio: torch.Tensor
        audio for which spectrogram needs to be calculated. It needs to be a mono audio
        as a torch tensor of shape (N,) where N is the total number of samples of the
        audio.

    Returns
    -------
    inner_html: str
        html code in string format to inject the audio related plots to the html report

    """
    audio_id = str(uuid.uuid4())  # nosec
    base_dir = "assets/stt"
    Path(base_dir).mkdir(parents=True, exist_ok=True)
    path_spec = os.path.join(base_dir, f"spec_{audio_id}.png")  # nosec
    path_waveform = os.path.join(base_dir, f"wavf_{audio_id}.png")  # nosec
    path_audio = os.path.join(base_dir, f"aud_{audio_id}.wav")  # nosec

    audio_numpy = audio.squeeze().cpu().numpy()
    save_spectrogram_plot(audio_numpy, path_spec, sampling_rate=16000)
    save_waveform_plot(audio_numpy, path_waveform, sampling_rate=16000)
    save_audio(audio_numpy, path_audio, sampling_rate=16000)

    inner_html = f"""
    <table style="display: block">
        <tbody>
            <tr>
                <td>
                    <img src={path_spec} height="150" width="150"></img>
                </td>
            </tr>
            <tr>
                <td>
                    <img src={path_waveform} height="75" width="150"></img>
                </td>
            </tr>
            <tr>
                <td>
                    <audio controls src={path_audio} style="display: block;width: 150px">
                        Your browser does not support the <code>audio</code> element.
                    </audio>
                </td>
            </tr>
        </tbody>
    </table>
    """
    return inner_html
