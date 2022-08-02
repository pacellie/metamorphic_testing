import os
from pathlib import Path
import soundfile  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np
import uuid
import torch
from typing import Union


class AudioVisualizer:
    def __init__(self, sampling_rate, base_dir):
        self.sampling_rate = sampling_rate
        self.base_dir = base_dir
        self.task_name = self.base_dir.split(os.sep)[-1]  # to know whether task is stt or aec
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)

    def save_spectrogram_plot(self, audio: np.ndarray, path: str) -> None:
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

        See Also
        --------
        save_waveform_plot: saves the waveform plot of an audio as an image
        save_audio: save the waveform audio as audio

        """
        plt.figure()
        plt.axis("off")
        plt.tight_layout()
        plt.specgram(audio, Fs=self.sampling_rate)
        plt.savefig(path, bbox_inches='tight')

    def save_waveform_plot(self, audio: np.ndarray, path: str) -> None:
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

        See Also
        --------
        save_spectrogram_plot: Saves the spectrogram plot of an audio as an image
        save_audio: save the waveform audio as audio

        """
        plt.figure()
        time = np.linspace(0, len(audio) / self.sampling_rate, num=len(audio))
        plt.axis("off")
        plt.tight_layout()
        plt.plot(time, audio, color="green")
        plt.savefig(path, bbox_inches='tight')

    def save_audio(self, audio: np.ndarray, path: str) -> None:
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

        See Also
        --------
        save_spectrogram_plot: Saves the spectrogram plot of an audio as an image
        save_waveform_plot: saves the waveform plot of an audio as an image

        """
        soundfile.write(path, audio, self.sampling_rate)

    def __call__(self, audio: Union[torch.Tensor, np.ndarray]) -> str:
        """
            Log and Visualize audio in the html test report

            Parameters
            ----------
            audio: Union[torch.Tensor, numpy.ndarray]
                audio for which spectrogram needs to be calculated. It needs to be a mono audio
                as a torch tensor or numpy ndarray of shape (N,) where N is the total number of
                samples of the audio.

            Returns
            -------
            inner_html: str
                html code in string format to inject the audio related plots to the html report

        """
        audio_id = str(uuid.uuid4())  # nosec
        path_spec = os.path.join(self.base_dir, f"spec_{audio_id}.png")  # nosec
        retrieve_path_spec = os.path.join("..", self.task_name, f"spec_{audio_id}.png")
        path_waveform = os.path.join(self.base_dir, f"wavf_{audio_id}.png")  # nosec
        retrieve_path_waveform = os.path.join(
            "..", self.task_name, f"wavf_{audio_id}.png")  # nosec
        path_audio = os.path.join(self.base_dir, f"aud_{audio_id}.wav")  # nosec
        retrieve_path_audio = os.path.join(
            "..", self.task_name, f"aud_{audio_id}.wav")  # nosec

        if torch.is_tensor(audio):
            audio = audio.squeeze().cpu().numpy()  # type: ignore
        self.save_spectrogram_plot(audio, path_spec)  # type: ignore
        self.save_waveform_plot(audio, path_waveform)  # type: ignore
        self.save_audio(audio, path_audio)  # type: ignore

        inner_html = f"""
            <table style="display: block">
                <tbody>
                    <tr>
                        <td>
                            <img src={retrieve_path_spec} height="150" width="150"></img>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <img src={retrieve_path_waveform} height="75" width="150"></img>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <audio 
                                controls 
                                src={retrieve_path_audio} 
                                style="display: block;width: 150px">
                                Your browser does not support the <code>audio</code> element.
                            </audio>
                        </td>
                    </tr>
                </tbody>
            </table>
            """
        return inner_html
