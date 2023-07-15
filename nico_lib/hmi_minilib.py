from __future__ import annotations
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
        self.hmi_output = np.zeros((480, 640, 3))
        self.hand_coords = [[0, 0], [0, 0]]

    def draw(self) -> None:
        """
        Output image generation, used to update the scene.
        """
        self.hmi_output = np.zeros((480, 640, 3))

        for obj in self.objects[::-1]:
            obj.draw(self.hmi_output)

        self._draw_hands()

        cv2.imshow("HMI", self.hmi_output)

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

    def add_object(self, obj) -> None:
        """
        Append object passed in argument into the drawing list.
        :param obj: Object to append to list.
        """
        self.objects.append(obj)

    def delete_object(self, obj_id) -> None:
        """
        Deletes object from GUI.
        :param obj_id: Index of the object to delete in object list.
        """
        if self.objects[obj_id].deletable:
            self.objects.pop(obj_id)


class Element:
    def __init__(self,
                 position: list | np.ndarray,
                 hit_box_dims: list | tuple = (20, 20),
                 color: tuple | list | np.ndarray = (1, 1, 1),
                 can_be_grabbed: bool = True,
                 deletable: bool = True) -> None:
        """
        Base class for GUI object, the draw function needs to be implemented in the subclass.
        :param position: initial position of the object on the GUI.
        :param hit_box_dims: [x, y] distance from center.
        :param color: object color.
        :param can_be_grabbed: condition for the object to be displaced by grabbing it.
        :param deletable: condition for the object to be deleted.
        """
        self.hit_box = hit_box_dims
        self.position = position
        self.color = color
        self.can_by_grabbed = can_be_grabbed
        self.deletable = deletable
        self.grabbed = False
        self.grabbed_by = 0

    def set_position(self, position: list | np.ndarray) -> None:
        """
        Overwrites the position of the object.
        :param position: [x, y] coordinates in the GUI.
        """
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


class Ball(Element):
    def __init__(self,
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
        super().__init__(position=initial_position,
                         color=color,
                         hit_box_dims=(ball_radius, ball_radius),
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.ball_radius = ball_radius

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        cv2.circle(src,
                   center=self.position,
                   radius=self.ball_radius,
                   color=tuple(self.color),
                   thickness=-1)


class Box(Element):
    def __init__(self, initial_position: list | np.ndarray,
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
        super().__init__(position=initial_position,
                         color=color,
                         hit_box_dims=[box_size[0] // 2, box_size[1] // 2],
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.box_size = box_size

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        cv2.rectangle(src,
                      pt1=(self.position[0] - self.box_size[0] // 2, self.position[1] - self.box_size[1] // 2),
                      pt2=(self.position[0] + self.box_size[0] // 2, self.position[1] + self.box_size[1] // 2),
                      color=self.color,
                      thickness=-1,
                      lineType=cv2.LINE_4)


class Text(Element):
    def __init__(self, initial_position: list | np.ndarray,
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
        super().__init__(position=initial_position,
                         color=color,
                         hit_box_dims=[font_size*len(text)*7, font_size*20],
                         can_be_grabbed=can_be_grabbed,
                         deletable=deletable)
        self.text = text
        self.font_size = font_size
        self.font = cv2_font

    def draw(self, src) -> None:
        """
        Shows object on GUI, meant to be used into an update function only.
        :param src: image to be drawn to.
        """
        cv2.putText(src,
                    text=self.text,
                    org=[self.position[0] - self.hit_box[0], self.position[1]],
                    fontFace=self.font,
                    fontScale=self.font_size,
                    color=self.color)


if __name__ == '__main__':
    pass
