import logging
from pathlib import Path
from typing import List
import uuid

import numpy as np
import cv2  # type: ignore
import albumentations  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pytest

# mypy complains that cv2 (and torchvision) has no stubs / not PEP 561-compliant
# thus is skipped. Same with matplotlib in classifier. Should we ignore?
# more info: https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports
from numpy import ndarray

from .classifier import read_traffic_signs, TrafficSignClassifier

from metamorphic_test import (
    transformation,
    relation,
    metamorphic,
    system,
    randomized,
)
from metamorphic_test.generators import RandInt, RandFloat
from metamorphic_test.relations import equality

brightness = metamorphic("brightness", relation=equality)
contrast = metamorphic("contrast", relation=equality)
both_transform = metamorphic("both_transform", relation=equality)
both_cv2 = metamorphic("both_cv2", relation=equality)
rain = metamorphic("rain", relation=equality)
snow = metamorphic("snow", relation=equality)
fog = metamorphic("fog", relation=equality)
gamma = metamorphic("gamma", relation=equality)
equalize = metamorphic("equalize", relation=equality)
downscale = metamorphic("downscale", relation=equality)
noise = metamorphic("noise", relation=equality)
clahe = metamorphic("clahe", relation=equality)
blur = metamorphic("blur", relation=equality)
dropout = metamorphic("dropout", relation=equality)
posterize = metamorphic("posterize", relation=equality)
horizontal_flip = metamorphic("horizontal_flip")
vertical_flip = metamorphic("vertical_flip")

pair = metamorphic("hflip_equalize")
trio = metamorphic("drop_down_bright", relation=equality)


"""
This example demonstrates MR tests of a traffic sign classifier NN:
- if the images are pertubed slightly, the prediction should not differ by much.
- if the perturbation causes the semantic information to change,
  e.g. from left to right turn, the prediction should reflect this change.

What follows here are 16 image perturbation functions, all with the same signature: receives
an image, and one or more parameters that can be used on the perturbation function.
Consult albumentations documentation for more information on functions that uses them:
https://albumentations.ai/docs/api_reference/augmentations/transforms/.
Note that the randomization of some of the parameters are delegated into our own framework
instead of using the perturbation's own random functionality.
For demonstration purposes, two MR tests will make use of two or three of these
perturbations in random sequence.
"""


@transformation(brightness)
@transformation(both_transform)
@randomized("beta", RandInt(-1, 1))
def brightness_adjustments(image: ndarray, beta: int) -> ndarray:
    return np.clip(image + beta, 0, 255).astype(np.uint8)


@transformation(contrast)
@transformation(both_transform)
@randomized("alpha", RandFloat(0.6, 1.5))
def contrast_adjustments(image: ndarray, alpha: float) -> ndarray:
    return np.clip(alpha * image, 0, 255).astype(np.uint8)


@transformation(both_cv2)
@randomized("alpha", RandFloat(0.6, 1.5))
@randomized("beta", RandInt(-1, 1))
def cv2_brightness_contrast_adjustments(
    image: ndarray, alpha: float, beta: int
) -> ndarray:
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


@transformation(rain)
@randomized("slant", RandInt(-5, 5))
def album_rain(
    image: ndarray,
    slant: int = 0,
    drop_length: int = 9,
    drop_width: int = 1,
    blur_value: int = 3,
) -> ndarray:
    image_transform = albumentations.RandomRain(
        slant_lower=slant,
        slant_upper=slant,
        drop_length=drop_length,
        drop_width=drop_width,
        blur_value=blur_value,
        p=1,
    )
    return image_transform.apply(image)


@transformation(snow)
@randomized("snow_point", RandFloat(0.1, 0.2))
def album_snow(
    image: ndarray, snow_point: float = 0.2, brightness_coeff: float = 2
) -> ndarray:
    image_transform = albumentations.RandomSnow(
        snow_point_lower=snow_point,
        snow_point_upper=snow_point,
        brightness_coeff=brightness_coeff,
        p=1,
    )
    return image_transform.apply(image)


@transformation(fog)
@randomized("fog_coef", RandFloat(0.3, 0.5))
def album_fog(
    image: ndarray, fog_coef: float = 0.5, alpha_coef: float = 0.08
) -> ndarray:
    image_transform = albumentations.RandomFog(
        fog_coef_lower=fog_coef, fog_coef_upper=fog_coef, alpha_coef=alpha_coef, p=1
    )
    return image_transform.apply(image)


@transformation(posterize)
@randomized("bits", RandInt(5, 7))
def album_posterize(image: ndarray, bits: int = 5) -> ndarray:
    image_transform = albumentations.Posterize(num_bits=bits, p=1)
    return image_transform.apply(image)


@transformation(gamma)
@randomized("limit", RandInt(70, 130))
def album_gamma(image: ndarray, limit: int = 101) -> ndarray:
    # some transform need a little different setup
    image_transform = albumentations.Compose(
        [albumentations.RandomGamma(gamma_limit=(limit, limit), p=1)]
    )
    return image_transform(image=image)["image"]


@transformation(equalize)
@transformation(pair)
def album_equalize(image: ndarray) -> ndarray:
    image_transform = albumentations.Equalize(p=1)
    return image_transform.apply(image)


@transformation(dropout)
@transformation(trio)
@randomized("holes", RandInt(4, 6))
def album_dropout(
    image: ndarray, holes: int = 6, height: int = 6, width: int = 6
) -> ndarray:
    # some transform need a little different setup
    image_transform = albumentations.Compose(
        [
            albumentations.CoarseDropout(
                max_holes=holes, max_height=height, max_width=width, p=1
            )
        ]
    )
    return image_transform(image=image)["image"]


@transformation(downscale)
@transformation(trio)
@randomized("scale", RandFloat(0.5, 0.7))
def album_downscale(image: ndarray, scale: float = 0.5) -> ndarray:
    image_transform = albumentations.Downscale(p=1)
    return image_transform.apply(image, scale=scale, interpolation=0)


@transformation(noise)
@randomized("color_shift", RandFloat(0.02, 0.04))
def album_ISONoise(
    image: ndarray, color_shift: float = 0.03, intensity: float = 0.3
) -> ndarray:
    image_transform = albumentations.ISONoise(
        color_shift=(color_shift, color_shift), intensity=(intensity, intensity), p=1
    )
    return image_transform.apply(image)


@transformation(clahe)
@transformation(trio)
@randomized("clip_limit", RandFloat(3.0, 3.5))
def album_CLAHE(
    image: ndarray, clip_limit: float = 3.0, tile_grid_size: int = 8
) -> ndarray:
    image_transform = albumentations.CLAHE(
        clip_limit=(clip_limit, clip_limit),
        tile_grid_size=(tile_grid_size, tile_grid_size),
        p=1,
    )
    return image_transform.apply(image)


@transformation(blur)
@randomized("kernel_size", RandInt(3, 5))
def album_blur(image: ndarray, kernel_size: int = 3) -> ndarray:
    image_transform = albumentations.Blur(blur_limit=[kernel_size, kernel_size], p=1)
    return image_transform.apply(image)


@transformation(horizontal_flip)
@transformation(pair)
def album_horizonflip(image: ndarray) -> ndarray:
    image_transform = albumentations.HorizontalFlip(p=1)
    return image_transform.apply(image)


@transformation(vertical_flip)
def album_verticalflip(image: ndarray) -> ndarray:
    image_transform = albumentations.VerticalFlip(p=1)
    return image_transform.apply(image)


@relation(horizontal_flip, vertical_flip, pair)
def flip_sign(x: int, y: int) -> bool:
    mapping = {16: 10, 10: 16, 38: 39, 39: 38, 33: 34, 34: 33, 25: 27, 27: 25}
    xhat = mapping.get(x, x)
    return equality(xhat, y)


class ExceptionLogger:
    """Class to help log exceptions that occur when saving images for visualization."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def logexception_geterrorstring(self, e: Exception) -> str:
        self.logger.error(e)
        return f"Failed to save image: {str(e)}"


# setup
test_images: List[ndarray] = read_traffic_signs()
classifier_under_test: TrafficSignClassifier = TrafficSignClassifier()
e_log: ExceptionLogger = ExceptionLogger()


def visualize_input(image: ndarray) -> str:
    """
    Use this visualization function if the Flask server is not used

    Parameters
    ----------
    image : ndarray
        image to visualize

    Returns
    -------
    html string that refers to the saved image
    """
    path = str(Path("assets") / f"img{uuid.uuid4()}.png")
    try:
        plt.imsave(path, image)
    except Exception as e:
        return e_log.logexception_geterrorstring(e)
    return f"<img src='{path}' width='50' height='50'>"


def visualize_input_webapp(image: ndarray) -> str:
    """
    Use this visualization function if the Flask server is used

    Parameters
    ----------
    image : ndarray
        image to visualize

    Returns
    -------
    html string that refers to the saved image
    """
    image_name = f"img{uuid.uuid4()}.png"
    base_dir = Path("assets/img")  # for web app
    base_dir.mkdir(parents=True, exist_ok=True)
    write_path = base_dir / image_name
    read_path = Path("../img") / image_name
    try:
        plt.imsave(write_path, image)
    except Exception as e:
        return e_log.logexception_geterrorstring(e)
    return f"<img src='{read_path}' width='50' height='50'>"


def visualize_output(label: int) -> str:
    """Obtain human readable name from a traffic sign class."""
    LABEL_NAMES = {
        16: "truck driving left",
        10: "truck driving right",
        11: "priority in traffic (next crossing)",
        12: "priority in traffic (road)",
        18: "warning",
        35: "straight road",
        38: "drive right",
        39: "drive left",
        33: "right turn",
        34: "left turn",
        25: "construction site right",
        27: "construction site left",
        28: "children crossing",
    }
    return LABEL_NAMES.get(label, f"unknown: {label}")


@pytest.mark.parametrize("image", test_images)
@system(visualize_input=visualize_input_webapp, visualize_output=visualize_output)
def test_image_classifier(image: ndarray) -> int:
    """Predict the traffic sign in an image"""
    return classifier_under_test.evaluate_image(image)
