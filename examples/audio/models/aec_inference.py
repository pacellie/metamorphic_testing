import os
import torch
from pathlib import Path

from examples.audio.utils.aec_utils import move_data_to_device  # type: ignore
from examples.audio.models.aec_core import Cnn14  # type: ignore


labels = []
with open(os.path.join(os.path.dirname(__file__), "labels.txt"), "r", encoding="utf-8") as f:
    for line in f:
        labels.append(line[:-1])


def create_folder(fd):
    if not os.path.exists(fd):
        os.makedirs(fd)


def get_filename(path):
    path = os.path.realpath(path)
    na_ext = path.split('/')[-1]
    na = os.path.splitext(na_ext)[0]
    return na


class AudioTagging:
    def __init__(self, model=None, checkpoint_path=None, device='cuda'):
        """Audio tagging inference wrapper.
        """
        if not checkpoint_path:
            checkpoint_path = f'{str(Path.home())}/panns_data/Cnn14_mAP=0.431.pth'

        if not os.path.exists(checkpoint_path) or os.path.getsize(checkpoint_path) < 3e8:
            create_folder(os.path.dirname(checkpoint_path))
            url = 'https://zenodo.org/record/3987831/files/Cnn14_mAP%3D0.431.pth?download=1'
            torch.hub.download_url_to_file(url, dst=checkpoint_path)

        if device == 'cuda' and torch.cuda.is_available():
            self.device = 'cuda'
        else:
            self.device = 'cpu'

        # Model
        if model is None:
            self.model = Cnn14(
                sample_rate=32000,
                model_config=(1024, 320, 64, 50, 14000),
                classes_num=527
            )
        else:
            self.model = model

        checkpoint = torch.load(checkpoint_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model'])

        # Parallel
        if 'cuda' in str(self.device):
            self.model.to(self.device)
            self.model = torch.nn.DataParallel(self.model)

    def inference(self, audio):
        audio = move_data_to_device(audio, self.device)

        with torch.no_grad():
            self.model.eval()
            output_dict = self.model(audio, None)

        clipwise_output = output_dict['clipwise_output'].data.cpu().numpy()
        embedding = output_dict['embedding'].data.cpu().numpy()

        return clipwise_output, embedding
