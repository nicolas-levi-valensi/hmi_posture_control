from __future__ import annotations
from typing import Callable
import cv2
import numpy as np


class GUI:
    def __init__(self,
                 window_name: str = "HMI") -> None:
        """
        Basic interface handling the displacement, adding and deleting of object of Element subclasses.
        :param window_name: GUI window name.
        """
        self.window_name = window_name
        self.objects = []
        self.background = np.zeros((480, 640, 3))
        self.hmi_output = self.background
        self.hand_coords = [[0, 0], [0, 0]]

    def draw(self) -> None:
        """
        Output image generation, used to update the scene.
        """
        self.hmi_output = self.background.copy()

        for obj in self.objects[::-1]:
            obj.draw(self.hmi_output)

        self._draw_hands()

        cv2.imshow("HMI", cv2.resize(self.hmi_output,
                                     (int(self.hmi_output.shape[1] * 1.5), int(self.hmi_output.shape[0] * 1.5))))

    def _draw_hands(self) -> None:
        """
        Hands positions drawing.
        """
        cv2.circle(self.hmi_output,
                   center=self.hand_coords[0],
                   radius=10,
                   color=(0.5, 0.5, 0),
                   thickness=3,
                   lineType=cv2.LINE_4)

        cv2.circle(self.hmi_output,
                   center=self.hand_coords[1],
                   radius=10,
                   color=(0, 0.5, 0.5),
                   thickness=3,
                   lineType=cv2.LINE_4)

    def set_hands_coords(self, coords: list) -> None:
        """
        Update the hand coordinates to control GUI.
        :param coords: 2x2 list of hand coordinates based on image shape.
        """
        self.hand_coords = coords

    def add_object(self, obj: Element) -> None:
        """
        Append object passed in argument into the drawing list.
        :param obj: Object to append to list.
        """
        if obj.position[0] - obj.hit_box[0] > 0 and obj.position[1] - obj.hit_box[1] > 0 \
                and obj.position[0] + obj.hit_box[0] < obj.master.hmi_output.shape[1] \
                and obj.position[1] + obj.hit_box[1] < obj.master.hmi_output.shape[0]:
            self.objects.append(obj)

    def delete_object(self, obj_id) -> None:
        """
        Deletes object from GUI.
        :param obj_id: Index of the object to delete in object list.
        """
        if self.objects[obj_id].deletable:
            self.objects.pop(obj_id)

    def set_background(self, path: str) -> None:
        self.background = cv2.resize(cv2.imread(path), (640, 480)) / 255


class Element:
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 hit_box_dims: list | tuple = (20, 20),
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
        Base class for GUI object, the draw function needs to be implemented in the subclass.
        :param initial_position: initial position of the object on the GUI.
        :param hit_box_dims: [x, y] distance from center.
        :param can_be_grabbed: condition for the object to be displaced by grabbing it.
        :param deletable: condition for the object to be deleted.
        """
        self.master = master
        self.hit_box = hit_box_dims
        self.position = initial_position
        self.can_by_grabbed = can_be_grabbed
        self.deletable = deletable
        self.grabbed = False
        self.grabbed_by = 0

    def set_position(self, position: list | np.ndarray) -> None:
        """
        Overwrites the position of the object.
        :param position: [x, y] coordinates in the GUI.
        """

        # Out of range avoidance
        if position[0] - self.hit_box[0] > 0 and position[1] - self.hit_box[1] > 0 \
                and position[0] + self.hit_box[0] < self.master.hmi_output.shape[1] \
                and position[1] + self.hit_box[1] < self.master.hmi_output.shape[0]:
            self.position = position

    def get_position(self) -> list:
        """
        Get the position of the object into the GUI coordinates.
        :return: position of the object.
        """
        return self.position

    def set_grabbed(self, grabbed: bool, holder_index: int = 0):
        """
        Set the grabbed state and the holder index of the object.
        :param grabbed: grabbed bool for state.
        :param holder_index: holder index
        """
        if self.can_by_grabbed:
            self.grabbed = grabbed
            self.grabbed_by = holder_index

    def is_grabbed(self) -> bool:
        """
        Returns the state of the object.
        :return: grabbed state of the object.
        """
        return self.grabbed

    def get_hit_box(self) -> (tuple | list):
        """
        Returns the dimensions of the object interaction hit box.
        :return: [x, y] distance from center.
        """
        return self.hit_box

    def click(self):
        pass


class Ball(Element):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 ball_radius: int = 30,
                 color: tuple | list | np.ndarray = (1, 1, 1),
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
        Basic ball based on Element class.
        :param initial_position: initial position of the object on the GUI.
        :param ball_radius: ball radius
        :param color: ball color
        :param can_be_grabbed: condition for the object to be displaced by grabbing it.
        :param deletable: condition for the object to be deleted.
        """
        super().__init__(master=master,
                         initial_position=initial_position,
                         hit_box_dims=(ball_radius, ball_radius),
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.ball_radius = ball_radius
        self.color = color

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        if not self.grabbed:
            cv2.circle(src,
                       center=self.position,
                       radius=self.ball_radius,
                       color=self.color,
                       thickness=-1)
        else:
            cv2.circle(src,
                       center=self.position,
                       radius=int(1.2 * self.ball_radius),
                       color=[c / 2 for c in self.color],
                       thickness=-1)


class Box(Element):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 box_size: tuple | list | np.ndarray = (100, 40),
                 color: tuple | list | np.ndarray = (1, 1, 1),
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
        Basic rectangle based on Element class.
        :param initial_position: initial position of the object on the GUI.
        :param box_size: box dimensions.
        :param color: rectangle color.
        :param can_be_grabbed: condition for the object to be displaced by grabbing it.
        :param deletable: condition for the object to be deleted.
        """
        super().__init__(master=master,
                         initial_position=initial_position,
                         hit_box_dims=[box_size[0] // 2, box_size[1] // 2],
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.box_size = box_size
        self.color = color

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        if not self.grabbed:
            cv2.rectangle(src,
                          pt1=(self.position[0] - self.box_size[0] // 2, self.position[1] - self.box_size[1] // 2),
                          pt2=(self.position[0] + self.box_size[0] // 2, self.position[1] + self.box_size[1] // 2),
                          color=self.color,
                          thickness=-1,
                          lineType=cv2.LINE_4)
        else:
            cv2.rectangle(src,
                          pt1=(self.position[0] - self.box_size[0] // 2, self.position[1] - self.box_size[1] // 2),
                          pt2=(self.position[0] + self.box_size[0] // 2, self.position[1] + self.box_size[1] // 2),
                          color=[c / 2 for c in self.color],
                          thickness=-1,
                          lineType=cv2.LINE_4)


class Text(Element):
    def __init__(self,
                 master: GUI, initial_position: list | np.ndarray,
                 text: str = "Basic text",
                 cv2_font: int = cv2.FONT_HERSHEY_COMPLEX_SMALL,
                 font_size: int | float = 1,
                 color: tuple | list | np.ndarray = (1, 1, 1),
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
        Basic text based on Element class.
        :param initial_position: initial position of the object on the GUI.
        :param text: displayed text.
        :param font_size: font size.
        :param color: rectangle color.
        """
        super().__init__(master=master,
                         initial_position=initial_position,
                         hit_box_dims=[font_size * len(text) * 7, font_size * 20],
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.text = text
        self.font_size = font_size
        self.font = cv2_font
        self.color = color

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        if not self.grabbed:
            cv2.putText(src,
                        text=self.text,
                        org=[self.position[0] - self.hit_box[0], self.position[1]],
                        fontFace=self.font,
                        fontScale=self.font_size,
                        color=self.color)
        else:
            cv2.putText(src,
                        text=self.text,
                        org=[self.position[0] - self.hit_box[0], self.position[1]],
                        fontFace=self.font,
                        fontScale=self.font_size * 1.1,
                        color=[c for c in self.color])


class Image(Element):
    def __init__(self,
                 master: GUI,
                 initial_position: list | np.ndarray,
                 image: np.ndarray,
                 image_shape: tuple | list | np.ndarray,
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
            Image based on Element class.
            :param initial_position: initial position of the object on the GUI.
            :param image_shape: image dimensions.
            :param can_be_grabbed: condition for the object to be displaced by grabbing it.
            :param deletable: condition for the object to be deleted.
            """
        super().__init__(master=master,
                         initial_position=initial_position,
                         hit_box_dims=[image_shape[0] // 2, image_shape[1] // 2],
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.shape = image_shape
        self.image = cv2.resize(image, self.shape)

    def draw(self, src):
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        if self.image.shape[2] == 4:
            for c in range(3):
                src[self.position[1] - self.shape[1] // 2:self.position[1] - self.shape[1] // 2 + self.shape[1],
                    self.position[0] - self.shape[0] // 2:self.position[0] - self.shape[0] // 2 + self.shape[0],
                    c] = (self.image[:, :, c] * self.image[:, :, 3] + (1 - self.image[:, :, 3]) *
                          src[self.position[1] - self.shape[1]//2:self.position[1] - self.shape[1]//2 + self.shape[1],
                              self.position[0] - self.shape[0]//2:self.position[0] - self.shape[0]//2 + self.shape[0],
                              c])
        else:
            src[self.position[1] - self.shape[1] // 2:self.position[1] - self.shape[1] // 2 + self.shape[1],
                self.position[0] - self.shape[0] // 2:self.position[0] - self.shape[0] // 2 + self.shape[0]] \
                = self.image


class ImageButton(Image):
    def __init__(self, master: GUI, initial_position: list | np.ndarray, command: Callable,
                 image: np.ndarray, image_shape: list | np.ndarray, can_be_grabbed: bool = False,
                 deletable: bool = False):
        super().__init__(master=master, initial_position=initial_position, image=image, image_shape=image_shape,
                         can_be_grabbed=can_be_grabbed, deletable=deletable)
        self.command = command

    def click(self):
        self.command()


if __name__ == '__main__':
    pass
