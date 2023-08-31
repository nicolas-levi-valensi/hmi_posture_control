from __future__ import annotations
import cv2
import numpy as np
from utils.hmi_minilib import GUI, Image


class Boy(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Town/char_0.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [40, 40]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Girl(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Town/char_1.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [40, 40]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Pirate0(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Town/pirate_0.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [32, 32]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
