import numpy as np
import torch
from typing import Union


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

        self.model, self.decoder, _ = torch.hub.load(
            repo_or_dir=self.repo,
            model=self.model_name,
            language=self.language,  # also available 'de', 'es'
            device=self.device
        )

    def recognize(self, audio: Union[torch.Tensor, np.ndarray]) -> str:
        if audio.ndim == 1:
            audio = audio.reshape(1, -1)
        else:
            assert audio.ndim == 2, f"Input audio must have either 1 or 2 dimension. " \
                                    f"But received {audio.ndim} instead"
            assert audio.shape[0] == 1, f"stereo audio is not supported. " \
                                        f"First dimension must be singleton. " \
                                        f"But received {audio.shape[0]} instead."
        if not torch.is_tensor(audio):
            assert isinstance(audio, np.ndarray), "input audio must be of type " \
                                                  "numpy.ndarray or torch.Tensor."
            audio = torch.from_numpy(audio)

        intermediate = self.model(audio).squeeze(0)

        recognized_text = self.decoder(intermediate.cpu())

        return recognized_text
