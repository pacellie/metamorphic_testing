from pathlib import Path
import random

import numpy as np
import cv2  # type: ignore
import albumentations  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pytest
# mypy complains that cv2 (and torchvision) has no stubs / not PEP 561-compliant
# thus is skipped. Same with matplotlib in classifier. Should we ignore?
# more info: https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-imports

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

brightness = metamorphic('brightness', relation=equality)
contrast = metamorphic('contrast', relation=equality)
both_transform = metamorphic('both_transform', relation=equality)
both_cv2 = metamorphic('both_cv2', relation=equality)
rain = metamorphic('rain', relation=equality)
snow = metamorphic('snow', relation=equality)
fog = metamorphic('fog', relation=equality)
gamma = metamorphic('gamma', relation=equality)
equalize = metamorphic('equalize', relation=equality)
downscale = metamorphic('downscale', relation=equality)
noise = metamorphic('noise', relation=equality)
clahe = metamorphic('clahe', relation=equality)
blur = metamorphic('blur', relation=equality)
horizontal_flip = metamorphic('horizontal_flip')
vertical_flip = metamorphic('vertical_flip')


@transformation(brightness)
@transformation(both_transform)
@randomized('beta', RandInt(-1, 1))
def brightness_adjustments(image, beta):
    return np.clip(image + beta, 0, 255).astype(np.uint8)
# to make some failing test with this brightness MR, add these 2 lines in the GT csv
# 00003.ppm;27;29;5;5;22;24;33
# 00008.ppm;45;50;6;5;40;45;25


@transformation(contrast)
@transformation(both_transform)
@randomized('alpha', RandFloat(0.6, 1.5))
def contrast_adjustments(image, alpha):
    return np.clip(alpha * image, 0, 255).astype(np.uint8)


@transformation(both_cv2)
@randomized('alpha', RandFloat(0.6, 1.5))
@randomized('beta', RandInt(-1, 1))
def cv2_brightness_and_contrast_adjustments(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


@transformation(rain)
@randomized('slant', RandInt(-5, 5))
def album_rain(image, slant=0, drop_length=9, drop_width=1, blur_value=3):
    image_transform = albumentations.RandomRain(
        slant_lower=slant,
        slant_upper=slant,
        drop_length=drop_length,
        drop_width=drop_width,
        blur_value=blur_value,
        p=1)
    return image_transform.apply(image)


@transformation(snow)
@randomized('snow_point', RandFloat(0.1, 0.2))
def album_snow(image, snow_point=0.2, brightness_coeff=2):
    image_transform = albumentations.RandomSnow(
        snow_point_lower=snow_point,
        snow_point_upper=snow_point,
        brightness_coeff=brightness_coeff,
        p=1)
    return image_transform.apply(image)


@transformation(fog)
@randomized('fog_coef', RandFloat(0.3, 0.5))
def album_fog(image, fog_coef=0.5, alpha_coef=0.08):
    image_transform = albumentations.RandomFog(
        fog_coef_lower=fog_coef,
        fog_coef_upper=fog_coef,
        alpha_coef=alpha_coef,
        p=1)
    return image_transform.apply(image)


# posterize doesn't seem to work properly, check later
# poster = metamorphic('poster', relation=equality)
# @transformation(poster)
# @randomized('bits', RandInt(5, 7))
# def album_posterize(image, bits=5):
#     image_transform = albumentations.Posterize(num_bits=bits, p=1)
#     return image_transform.apply(image)


@transformation(gamma)
@randomized('limit', RandInt(100, 110))
def album_gamma(image, limit=101):
    image_transform = albumentations.RandomGamma(gamma_limit=(limit, limit), p=1)
    return image_transform.apply(image)


@transformation(equalize)
def album_equalize(image):
    image_transform = albumentations.Equalize(p=1)
    return image_transform.apply(image)


# find out: which one doesn't work if just apply
# add coarse dropout, and change to go via transform since basic apply does nothing


@transformation(downscale)
@randomized('scale', RandFloat(0.6, 0.8))
def album_downscale(image, scale=0.5):
    image_transform = albumentations.Downscale(p=1)
    return image_transform.apply(image, scale=scale, interpolation=0)


@transformation(noise)
@randomized('color_shift', RandFloat(0.02, 0.04))
def album_ISONoise(image, color_shift=0.03, intensity=0.3):
    image_transform = albumentations.ISONoise(
        color_shift=(color_shift, color_shift),
        intensity=(intensity, intensity),
        p=1)
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
@randomized('kernel_size', RandInt(3, 5))
def album_blur(image, kernel_size=3):
    image_transform = albumentations.Blur(blur_limit=[kernel_size, kernel_size], p=1)
    return image_transform.apply(image)


@transformation(horizontal_flip)
def album_horizonflip(image):
    image_transform = albumentations.HorizontalFlip(p=1)
    return image_transform.apply(image)


@transformation(vertical_flip)
def album_verticalflip(image):
    image_transform = albumentations.VerticalFlip(p=1)
    return image_transform.apply(image)


@relation(horizontal_flip, vertical_flip)
def flip_sign(x, y):
    mapping = {16: 10, 10: 16, 38: 39, 39: 38, 33: 34, 34: 33, 25: 27, 27: 25}
    xhat = mapping.get(x, x)
    return equality(xhat, y)


# setup
test_images, test_labels = read_traffic_signs()
classifier_under_test = TrafficSignClassifier()


def visualize(image):
    path = str(Path("assets") / f"img{random.randint(0, 1e10)}.png")  # nosec
    try:
        plt.imsave(path, image)
    except Exception as e:
        print(e)
    return f"""
    <img src="{path}" width="53" height="54">
"""


@pytest.mark.parametrize('image', test_images)
@system(horizontal_flip, visualize_input=visualize)
# brightness, contrast, both_transform, both_cv2, rain, snow, fog, gamma, equalize,
#        downscale, noise, clahe, blur, horizontal_flip, vertical_flip)
def test_image_classifier(image):
    return classifier_under_test.evaluate_image(image)
