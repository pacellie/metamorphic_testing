import logging
from pathlib import Path
from typing import Optional, List
import uuid
import torch
import numpy as np
import cv2  # type: ignore
import albumentations  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import pytest
from numpy import ndarray
from torch import Tensor
from torchvision import transforms  # type: ignore

from .keypoint_detection import read_keypoint_images, KeypointModel
from metamorphic_test import transformation, relation, metamorphic, system, randomized
from metamorphic_test.generators import RandInt, RandFloat

contrast = metamorphic("contrast")
brightness = metamorphic("brightness")
both_cv2 = metamorphic("both_cv2")
downscale = metamorphic("downscale")
dropout = metamorphic("dropout")
gamma = metamorphic("gamma")
equalize = metamorphic("equalize")
clahe = metamorphic("clahe")
blur = metamorphic("blur")


"""
This example demonstrates MR tests of a keypoint prediction NN on human portraits:
if the portraits are perturbed slightly, the prediction should not differ by much.

Be advised that the relation function makes use of this NN's training error function.
Other NN MR tests could apply the same principle, where the error between the first and
second output are small enough, using its own training error function.

What follows here are 9 image perturbation functions, all with the same signature: receives
an image, and one or more parameters that can be used on the perturbation function.
Consult albumentations documentation for more information on functions that uses them:
https://albumentations.ai/docs/api_reference/augmentations/transforms/.
Note that the randomization of some of the parameters are delegated into our own framework
instead of using the perturbation's own random functionality.
Also there are less perturbations that can be used here than the classifier example, as
there are perturbations that can only be applied on RGB image (portraits here are grayscale).
Flips are also not included as it is quite complicated to swap the predictions (some will
have to be mirrored like nose, others have to be swapped like left-right eye), and the
NN may not work properly from an upside-down portraits, in case of vertical flips
"""


@transformation(contrast)
@randomized("alpha", RandFloat(0.6, 1.5))
def contrast_adjustments(image: ndarray, alpha: float) -> ndarray:
    return np.clip(alpha * image, 0, 255).astype(np.uint8)


@transformation(brightness)
@randomized("beta", RandInt(-30, 30))
def brightness_adjustments(image: ndarray, beta: int) -> ndarray:
    return np.clip(image + beta, 0, 255).astype(np.uint8)


@transformation(both_cv2)
@randomized("alpha", RandFloat(0.6, 1.5))
@randomized("beta", RandInt(-30, 30))
def cv2_brightness_contrast_adjustments(
    image: ndarray, alpha: float, beta: int
) -> ndarray:
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


@transformation(dropout)
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
@randomized("scale", RandFloat(0.5, 0.7))
def album_downscale(image: ndarray, scale: float = 0.5) -> ndarray:
    image_transform = albumentations.Downscale(p=1)
    return image_transform.apply(image, scale=scale, interpolation=0)


@transformation(gamma)
@randomized("limit", RandInt(70, 130))
def album_gamma(image: ndarray, limit: int = 101) -> ndarray:
    # some transform need a little different setup
    image_transform = albumentations.Compose(
        [albumentations.RandomGamma(gamma_limit=(limit, limit), p=1)]
    )
    return image_transform(image=image)["image"]


@transformation(equalize)
def album_equalize(image: ndarray) -> ndarray:
    image_transform = albumentations.Equalize(p=1)
    return image_transform.apply(image)


@transformation(clahe)
@randomized("clip_limit", RandFloat(3.0, 3.5))
def album_CLAHE(image: ndarray, clip_limit=3.0, tile_grid_size: int = 8) -> ndarray:
    image_transform = albumentations.CLAHE(
        clip_limit=(clip_limit, clip_limit),
        tile_grid_size=(tile_grid_size, tile_grid_size),
        p=1,
    )
    return image_transform.apply(image)


@transformation(blur)
@randomized("kernel_size", RandInt(5, 7))
def album_blur(image: ndarray, kernel_size: int = 3) -> ndarray:
    image_transform = albumentations.Blur(blur_limit=[kernel_size, kernel_size], p=1)
    return image_transform.apply(image)


@relation(
    contrast, brightness, both_cv2, dropout, downscale, gamma, equalize, clahe, blur
)
def error_is_small(x: Tensor, y: Tensor) -> bool:
    """
    Determines if the resulting keypoints pairs are close or too far apart.

    This is measured using Mean-square-error loss function, which is the same loss function
    that is used to train this neural network by minimizing them.

    Parameters
    ----------
    x : Tensor
        The first set of keypoints
    y : Tensor
        The second set of keypoints

    Returns
    -------
    True if the keypoints are not far apart, False otherwise.
    """
    loss_fn = torch.nn.MSELoss()
    loss = loss_fn(y, x).item()
    return loss < 0.002


class KeypointVisualizer:
    """
    Visualizer class for the keypoint prediction.

    Recall that the MR framework provide ONLY the result of the model to the output
    visualizer, in this case, the Tensor containing the predicted coordinates.
    Unfortunately, unlike the image classifier visualizer, printing just the output
    coordinates (even if transformed) isn't exactly helpful. It is best to have it
    overlaid on top of the input image. The framework will call the input visualizer
    twice, one for the base, and another for the follow-up input, then the output
    visualizer twice with the same order. This class will keep track of the last
    two input image to use along with the output visualizer.
    """

    def __init__(self) -> None:
        self.transform = transforms.ToTensor()
        self.first_input: Optional[ndarray] = None
        self.second_input: Optional[ndarray] = None
        self.first_is_next: bool = True
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    def logexception_geterrorstring(self, e: Exception) -> str:
        self.logger.error(e)
        return f"Failed to save image: {str(e)}"

    def vis_input(self, image: ndarray) -> str:
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
        image = self.prepare_input_visual(image)
        path: str = str(Path("assets") / f"img{uuid.uuid4()}.png")
        try:
            plt.imsave(path, image, cmap="gray")
        except Exception as e:
            return self.logexception_geterrorstring(e)
        return f"<img src='{path}' width='100' height='100'>"

    def vis_input_app(self, image: ndarray) -> str:
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
        image = self.prepare_input_visual(image)
        image_name: str = f"img{uuid.uuid4()}.png"
        base_dir: Path = Path("assets/img")  # for web app
        base_dir.mkdir(parents=True, exist_ok=True)
        write_path: Path = base_dir / image_name
        read_path: Path = Path("../img") / image_name
        try:
            plt.imsave(write_path, image, cmap="gray")
        except Exception as e:
            return self.logexception_geterrorstring(e)
        return f"<img src='{read_path}' width='100' height='100'>"

    def prepare_input_visual(self, image: ndarray) -> ndarray:
        """Convert image into tensor of appropriate size, then store it either in
        the first or second slot."""
        image = (self.transform(image).clone() * 255).view(96, 96)
        if self.first_is_next:
            self.first_input = image
        else:
            self.second_input = image
        self.first_is_next = not self.first_is_next
        return image

    def vis_output(self, keypoints: Tensor) -> str:
        """
        Use this visualization function if the Flask server is not used

        Parameters
        ----------
        keypoints : tensor
            keypoints to visualize

        Returns
        -------
        html string that refers to the saved image
        """
        if not self.prepare_output_visual(keypoints):
            return str(keypoints)
        path: str = str(Path("assets") / f"img{uuid.uuid4()}.png")
        try:
            plt.savefig(path, bbox_inches="tight", pad_inches=0)
        except Exception as e:
            return self.logexception_geterrorstring(e)
        return f"<img src='{path}' width='100' height='100'>"

    def vis_output_app(self, keypoints: Tensor) -> str:
        """
        Use this visualization function if the Flask server is used

        Parameters
        ----------
        keypoints : tensor
            keypoints to visualize

        Returns
        -------
        html string that refers to the saved image
        """
        if not self.prepare_output_visual(keypoints):
            return str(keypoints)
        image_name: str = f"img{uuid.uuid4()}.png"
        base_dir: Path = Path("assets/img")  # for web app
        base_dir.mkdir(parents=True, exist_ok=True)
        write_path: Path = base_dir / image_name
        read_path: Path = Path("../img") / image_name
        try:
            plt.savefig(write_path, bbox_inches="tight", pad_inches=0)
        except Exception as e:
            return self.logexception_geterrorstring(e)
        return f"<img src='{read_path}' width='100' height='100'>"

    def prepare_output_visual(self, keypoints: Tensor) -> bool:
        """
        Clear matplotlib's canvas, then plot the keypoints overlaid on either the first
        or the second stored image, returning

        Parameters
        ----------
        keypoints : tensor
            keypoints to visualize

        Returns
        -------
        False if this method is somehow called before 2
        input images are stored, True otherwise.
        """
        plt.clf()
        if self.first_is_next:
            image = self.first_input
        else:
            image = self.second_input
        self.first_is_next = not self.first_is_next
        if image is None:
            return False
        plt.imshow(image, cmap="gray")
        keypoints = keypoints.clone() * 48 + 48
        plt.scatter(keypoints[:, 0], keypoints[:, 1], s=200, marker=".", c="m")
        plt.axis("off")
        return True


# setup
test_images: List[ndarray] = read_keypoint_images()
visualizer: KeypointVisualizer = KeypointVisualizer()
predictor_under_test: KeypointModel = KeypointModel()


@pytest.mark.parametrize("image", test_images)
@system(visualize_input=visualizer.vis_input_app, visualize_output=visualizer.vis_output_app)
def test_keypoint_predictor(image: ndarray) -> Tensor:
    """Predict the facial keypoints of a portrait"""
    return predictor_under_test.predict(image)
