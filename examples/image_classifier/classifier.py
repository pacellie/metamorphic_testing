# deep learning imports
from pathlib import Path
import csv
from typing import List

import matplotlib.pyplot as plt  # type: ignore

import torch
from numpy import ndarray
from torch import nn, Tensor
import torch.nn.functional as fun
import torchvision as tv  # type: ignore


def read_traffic_signs(rootpath: str = "data/") -> List[ndarray]:
    """
    Reads traffic sign pictures for German Traffic Sign Recognition Benchmark.

    Parameters
    ----------
    rootpath : str
        path to the traffic sign data, defaults to 'data/'

    Returns
    -------
    list of images
    """
    images: List[ndarray] = []  # images

    data_dir: Path = Path(__file__).parent / rootpath
    prefix: Path = data_dir / "GTSRB" / "Final_Test" / "Images"

    with open(
        data_dir / "GTSRB_Final_Test_GT" / "GT-final_test.csv", encoding="utf-8"
    ) as gt:
        gt_reader = csv.reader(gt, delimiter=";")  # csv parser for annotations file
        next(gt_reader)  # skip header
        # loop over all images in current annotations file
        for row in gt_reader:
            images.append(plt.imread(prefix / row[0]))  # the 0th column is the filename
    return images


class TrafficSignClassifier(nn.Module):
    """
    A neural network that receives images and determines the traffic sign in that image,
    e.g. left/right turn, priority, warning, etc.
    """

    def __init__(self) -> None:
        """
        Initialize the traffic sign classifier model.
        """
        super().__init__()

        # CNN layers
        self.conv1 = nn.Conv2d(3, 100, kernel_size=5)
        self.bn1 = nn.BatchNorm2d(100)
        self.conv2 = nn.Conv2d(100, 150, kernel_size=3)
        self.bn2 = nn.BatchNorm2d(150)
        self.conv3 = nn.Conv2d(150, 250, kernel_size=3)
        self.bn3 = nn.BatchNorm2d(250)
        self.conv_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(250 * 2 * 2, 350)
        self.fc2 = nn.Linear(350, 43)

        self.localization = nn.Sequential(
            nn.Conv2d(3, 8, kernel_size=7),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True),
            nn.Conv2d(8, 10, kernel_size=5),
            nn.MaxPool2d(2, stride=2),
            nn.ReLU(True),
        )

        # Regressor for the 3 * 2 affine matrix
        self.fc_loc = nn.Sequential(
            nn.Linear(10 * 4 * 4, 32), nn.ReLU(True), nn.Linear(32, 3 * 2)
        )

        # Initialize the weights/bias with identity transformation
        self.fc_loc[2].weight.data.zero_()
        self.fc_loc[2].bias.data.copy_(
            torch.tensor([1, 0, 0, 0, 1, 0], dtype=torch.float)
        )

        self.input_preprocessing_pipeline = tv.transforms.Compose(
            [
                tv.transforms.ToPILImage(),
                tv.transforms.Resize((64, 64)),
                tv.transforms.ToTensor(),
            ]
        )
        """Used to transform ndarray inputs into tensors of appropriate size and format"""

        self.eval()
        self.load_state_dict(
            torch.load(
                Path(__file__).parent / "model" / "classifier_pretrained_weights.pth",
                map_location=torch.device("cpu"),
            )
        )

    def stn(self, x: Tensor) -> Tensor:
        """Spatial transformer network forward function"""
        xs = self.localization(x)
        xs = xs.view(-1, 10 * 4 * 4)
        theta = self.fc_loc(xs)
        theta = theta.view(-1, 2, 3)
        grid = fun.affine_grid(theta, list(x.size()), align_corners=True)
        x = fun.grid_sample(x, grid, align_corners=True)
        return x

    def forward(self, x: Tensor) -> Tensor:
        """Process the image with the neural network."""
        # transform the input
        x = fun.interpolate(x, size=(32, 32), mode="bilinear")
        x = self.stn(x)

        # Perform forward pass
        x = self.bn1(fun.max_pool2d(fun.leaky_relu(self.conv1(x)), 2))
        x = self.conv_drop(x)
        x = self.bn2(fun.max_pool2d(fun.leaky_relu(self.conv2(x)), 2))
        x = self.conv_drop(x)
        x = self.bn3(fun.max_pool2d(fun.leaky_relu(self.conv3(x)), 2))
        x = self.conv_drop(x)
        x = x.view(-1, 250 * 2 * 2)
        x = fun.relu(self.fc1(x))
        x = fun.dropout(x, training=self.training)
        x = self.fc2(x)
        return fun.log_softmax(x, dim=1)

    def evaluate_image(self, img: ndarray) -> int:
        """Process the image with the neural network, and return the most likely class."""
        tensor_img: Tensor = self.input_preprocessing_pipeline(img)[None, :]
        logits: Tensor = self(tensor_img)
        return fun.softmax(logits, dim=1).max(dim=1)[1].item()
