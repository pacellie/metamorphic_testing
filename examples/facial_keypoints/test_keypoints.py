from pathlib import Path
import random
import torch

import numpy as np
import cv2  # type: ignore
import albumentations  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pytest
from torchvision import transforms

from .keypoint_detection import read_keypoint_images, KeypointModel

from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    randomized
)
from metamorphic_test.generators import RandInt, RandFloat

contrast = metamorphic('contrast')
brightness = metamorphic('brightness')
both_cv2 = metamorphic('both_cv2')
downscale = metamorphic('downscale')
dropout = metamorphic('dropout')
gamma = metamorphic('gamma')
equalize = metamorphic('equalize')
clahe = metamorphic('clahe')
blur = metamorphic('blur')


@transformation(contrast)
@randomized('alpha', RandFloat(0.6, 1.5))
def contrast_adjustments(image, alpha):
    return np.clip(alpha * image, 0, 255).astype(np.uint8)


@transformation(brightness)
@randomized('beta', RandInt(-30, 30))
def brightness_adjustments(image, beta):
    return np.clip(image + beta, 0, 255).astype(np.uint8)


@transformation(both_cv2)
@randomized('alpha', RandFloat(0.6, 1.5))
@randomized('beta', RandInt(-30, 30))
def cv2_brightness_and_contrast_adjustments(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


@transformation(dropout)
@randomized('holes', RandInt(4, 6))
def album_dropout(image, holes=6, height=6, width=6):
    # some transform need a little different setup
    image_transform = albumentations.Compose([
        albumentations.CoarseDropout(max_holes=holes, max_height=height, max_width=width, p=1)
    ])
    return image_transform(image=image)["image"]


@transformation(downscale)
@randomized('scale', RandFloat(0.5, 0.7))
def album_downscale(image, scale=0.5):
    image_transform = albumentations.Downscale(p=1)
    return image_transform.apply(image, scale=scale, interpolation=0)


@transformation(gamma)  # not expressive
@randomized('limit', RandInt(70, 130))
def album_gamma(image, limit=101):
    # some transform need a little different setup
    image_transform = albumentations.Compose([
        albumentations.RandomGamma(gamma_limit=(limit, limit), p=1)
    ])
    return image_transform(image=image)["image"]


@transformation(equalize)
def album_equalize(image):
    image_transform = albumentations.Equalize(p=1)
    return image_transform.apply(image)


@transformation(clahe)
@randomized('clip_limit', RandFloat(3.0, 3.5))
def album_CLAHE(image, clip_limit=3.0, tile_grid_size=8):
    image_transform = albumentations.CLAHE(
        clip_limit=(clip_limit, clip_limit),
        tile_grid_size=(tile_grid_size, tile_grid_size),
        p=1)
    return image_transform.apply(image)


@transformation(blur)
@randomized('kernel_size', RandInt(5, 7))
def album_blur(image, kernel_size=3):
    image_transform = albumentations.Blur(blur_limit=[kernel_size, kernel_size], p=1)
    return image_transform.apply(image)


@relation(contrast, brightness, both_cv2, dropout, downscale, gamma, equalize, clahe, blur)
def error_is_small(x, y):
    loss_fn = torch.nn.MSELoss()
    loss = loss_fn(y, x)
    print(loss)   # logger here
    return loss < 0.002


class KeypointVisualizer:
    def __init__(self):
        self.transform = transforms.ToTensor()
        self.first_input = None
        self.second_input = None
        self.first_is_next = True

    def vis_input(self, image):
        image = (self.transform(image).clone() * 255).view(96, 96)
        if self.first_is_next:
            self.first_input = image
        else:
            self.second_input = image
        self.first_is_next = not self.first_is_next
        path = str(Path("assets") / f"img{random.randint(0, 1e10)}.png")  # nosec
        try:
            plt.imsave(path, image, cmap='gray')
        except Exception as e:
            print(e)
        return f"""<img src="{path}" width="100" height="100">"""

    def vis_output(self, keypoints):
        if self.first_is_next:
            image = self.first_input
        else:
            image = self.second_input
        self.first_is_next = not self.first_is_next
        if image is None:
            return str(keypoints)
        path = str(Path("assets") / f"img{random.randint(0, 1e10)}.png")  # nosec
        plt.imshow(image, cmap="gray")
        keypoints = keypoints.clone() * 48 + 48
        plt.scatter(keypoints[:, 0], keypoints[:, 1], s=200, marker='.', c='m')
        plt.axis("off")
        plt.savefig(path, bbox_inches='tight',pad_inches = 0)
        plt.clf()
        return f"""<img src="{path}" width="100" height="100">"""


# setup
test_images = read_keypoint_images()
visualizer = KeypointVisualizer()
predictor_under_test = KeypointModel()


@pytest.mark.parametrize('image', test_images)
@system(contrast, brightness, both_cv2, dropout, downscale, gamma, equalize, clahe, blur,
        visualize_input=visualizer.vis_input, visualize_output=visualizer.vis_output)
def test_keypoint_predictor(image):
    return predictor_under_test.predict(image)
