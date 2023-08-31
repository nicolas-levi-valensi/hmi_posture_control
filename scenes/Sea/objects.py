from __future__ import annotations
import cv2
import numpy as np
from utils.hmi_minilib import GUI, Image


class Shark0(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/shark_00.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [200, 113]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Shark1(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/shark_01.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [200, 82]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Fish0(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/fish_00.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [90, 90]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Fish1(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/fish_01.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [110, 80]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Fish2(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/fish_02.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [100, 50]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Shell0(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/shell_02.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [80, 80]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Shell1(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Sea/shell_01.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [90, 70]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
