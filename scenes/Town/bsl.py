from utils.hmi_minilib import GUI
from scenes.Town.objects import Boy, Girl, Pirate0


def base_scene(gui_handler: GUI) -> None:
    gui_handler.set_background(path="Assets/sprites/Town/bg_town.png")

    gui_handler.add_object(Boy(master=gui_handler,
                               initial_position=[160, 160],
                               can_be_grabbed=True,
                               deletable=True))

    gui_handler.add_object(Girl(master=gui_handler,
                                initial_position=[300, 290],
                                can_be_grabbed=True,
                                deletable=True))

    gui_handler.add_object(Pirate0(master=gui_handler,
                                   initial_position=[280, 290],
                                   can_be_grabbed=True,
                                   deletable=True))


def mov_bind():
    return Boy, Girl


def town_scene_loader(gui_handler: GUI):
    base_scene(gui_handler)
    return mov_bind()
