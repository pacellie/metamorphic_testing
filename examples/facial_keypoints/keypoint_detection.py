from pathlib import Path
import pandas as pd
import numpy as np
from typing import List

import torch
from numpy import ndarray
from torch import nn, Tensor
from torchvision import transforms  # type: ignore


def read_keypoint_images(csv_name: str = "val.csv") -> List[ndarray]:
    """
    Reads portraits from supplied csv.

    Parameters
    ----------
    csv_name : str
        name of the csv file, defaults to 'val.csv'

    Returns
    -------
    list of portraits
    """
    images: List[ndarray] = []
    csv_file = Path(__file__).parent / csv_name
    key_pts_frame = pd.read_csv(csv_file)
    key_pts_frame.dropna(inplace=True)
    key_pts_frame.reset_index(drop=True, inplace=True)
    for idx in range(key_pts_frame.shape[0]):
        img_str = key_pts_frame.loc[idx]["Image"]
        img: ndarray = np.array([int(item) for item in img_str.split()]).reshape((96, 96))
        image: ndarray = np.expand_dims(img, axis=2).astype(np.uint8)
        images.append(image)
    return images


class KeypointModel(nn.Module):
    """A neural network that receives portraits and determines the location of facial
    keypoints, e.g. left/right eye, nose, lips, eyebrows, etc."""

    def __init__(self) -> None:
        """Initialize the keypoint model."""
        super().__init__()
        self.model: nn.Module = nn.Sequential(
            nn.Conv2d(1, 3, 3),
            nn.ReLU(),
            nn.Conv2d(3, 5, 3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(42320, 30),
        )
        """The architecture (weights, non-linearity, etc) of this neural network"""

        self.transform = transforms.ToTensor()
        """Used to transform ndarray inputs into torch tensors"""

        self.eval()
        self.load_state_dict(
            torch.load(
                Path(__file__).parent / "keypoint_pretrain_weights.pth",
                map_location=torch.device("cpu"),
            )
        )

    def forward(self, image: ndarray) -> Tensor:
        """Process the image with the neural network."""
        x: Tensor = self.transform(image)
        if x.dim() == 3:
            x = torch.unsqueeze(x, 0)
        return self.model(x)

    def predict(self, img: ndarray) -> Tensor:
        """Process the image with the neural network, and convert the result to coordinates of
        15 keypoints."""
        return torch.squeeze(self(img).detach()).view(15, 2)
