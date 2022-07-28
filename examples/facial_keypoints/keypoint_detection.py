# deep learning imports
import pickle
from pathlib import Path
import pandas as pd
import numpy as np
from typing import List, Tuple

import matplotlib.pyplot as plt   # type: ignore

import torch
from numpy import ndarray
from torch import nn, Tensor
import torch.nn.functional as fun
import torchvision as tv  # type: ignore
from torchvision import transforms


def read_keypoint_images(rootpath: str = "data/") -> List[Tensor]:
    """Reads traffic sign data for German Traffic Sign Recognition Benchmark.

    Arguments: path to the traffic sign data, for example './GTSRB/Training'
    Returns:   list of images, list of corresponding labels"""
    images = []  # images

    csv_file = Path(__file__).parent / "val.csv"
    key_pts_frame = pd.read_csv(csv_file)
    key_pts_frame.dropna(inplace=True)
    key_pts_frame.reset_index(drop=True, inplace=True)
    transform = transforms.ToTensor()

    # with open(data_dir / "GTSRB_Final_Test_GT/GT-final_test.csv", encoding="utf-8") as gt_file:
    #     gt_reader = csv.reader(gt_file, delimiter=";")  # csv parser for annotations file
    #     next(gt_reader)  # skip header
    #     # loop over all images in current annotations file
    #     for row in gt_reader:
    #         images.append(plt.imread(prefix / row[0]))  # the 0th column is the filename
    #         labels.append(row[7])  # the 8th column is the label
    for idx in range(1):
        img_str = key_pts_frame.loc[idx]['Image']
        img = np.array([int(item) for item in img_str.split()]).reshape((96, 96))
        image = np.expand_dims(img, axis=2).astype(np.uint8)
        # image = transform(image)
        images.append(image)

    return images


class KeypointModel(nn.Module):
    def __init__(self, eval_mode: bool = True) -> None:
        """
        Initialize your model from a given dict containing all your hparams
        Warning: Don't change the method declaration (i.e. by adding more
            arguments), otherwise it might not work on the submission server
        """
        super().__init__()
        self.hparams = {"batch_size": 256, "learning_rate": 1e-3}
        self.model = nn.Sequential(
            nn.Conv2d(1, 3, 3),
            nn.ReLU(),
            nn.Conv2d(3, 5, 3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(42320, 30)
        )

        self.transform = transforms.ToTensor()

        if eval_mode:
            self.eval()
            self.load_state_dict(
                torch.load(
                    Path(__file__).parent / "keypoint_pretrain_weights.pth",
                    map_location=torch.device("cpu")
                )
            )
            # state_and_hparams = pickle.load(open(Path(__file__).parent / "facial_keypoints.p", 'rb', 4))
            # self.load_state_dict(state_and_hparams["state_dict"])

    # Spatial transformer network forward function
    # def stn(self, x: Tensor) -> Tensor:
    #     xs = self.localization(x)
    #     xs = xs.view(-1, 10 * 4 * 4)
    #     theta = self.fc_loc(xs)
    #     theta = theta.view(-1, 2, 3)
    #     grid = fun.affine_grid(theta, list(x.size()), align_corners=True)
    #     x = fun.grid_sample(x, grid, align_corners=True)
    #     return x

    def forward(self, image: ndarray) -> Tensor:
        x = self.transform(image)
        if x.dim() == 3:
            x = torch.unsqueeze(x, 0)
        return self.model(x)

    def predict(self, img: Tensor) -> Tensor:
        return torch.squeeze(self(img).detach()).view(15, 2)
