from __future__ import annotations
import cv2
import numpy as np
from utils.hmi_minilib import GUI, ImageButton
from functools import partial


def edit_scene(name: str):
    global SCENE_TO_LOAD
    SCENE_TO_LOAD = name
    print(SCENE_TO_LOAD)


class StartButton(ImageButton):
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
                         deletable=deletable,
                         command=partial(edit_scene, "sea"))
