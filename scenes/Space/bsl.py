from utils.hmi_minilib import GUI
from scenes.Space.objects import Astronaut, Rocket, SpaceStation



def base_scene(gui_handler: GUI) -> None:
    gui_handler.set_background(path="Assets/sprites/Space/bg_space.jpg")

    gui_handler.add_object(Astronaut(master=gui_handler,
                                     initial_position=[450, 300],
                                     can_be_grabbed=True,
                                     deletable=True))

    gui_handler.add_object(Rocket(master=gui_handler,
                                  initial_position=[100, 300],
                                  can_be_grabbed=True,
                                  deletable=True))

    gui_handler.add_object(SpaceStation(master=gui_handler,
                                        initial_position=[400, 100],
                                        can_be_grabbed=True,
                                        deletable=False))


def mov_bind():
    return Astronaut, Rocket


def space_scene_loader(gui_handler: GUI):
    base_scene(gui_handler)
    return mov_bind()
