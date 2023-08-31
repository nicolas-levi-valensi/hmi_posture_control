from __future__ import annotations
import cv2
import numpy as np
from utils.hmi_minilib import GUI, Image


class Astronaut(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Space/astronaut.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [90, 80]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class Rocket(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Space/rocket.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [80, 80]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)


class SpaceStation(Image):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        image = cv2.imread("Assets/sprites/Space/space_station_2.png", cv2.IMREAD_UNCHANGED) / 255
        shape = [150, 150]

        super().__init__(master=master,
                         initial_position=initial_position,
                         image=image,
                         image_shape=shape,
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
