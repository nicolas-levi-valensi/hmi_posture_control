from utils.hmi_minilib import GUI, Text, Ball, Box, ImageButton
from scenes.Menu.objects import StartButton


def menu_scene(gui_handler: GUI) -> None:
    gui_handler.set_background(path="Assets/sprites/Menu/bg_menu.jpg")

    gui_handler.add_object(Text(master=gui_handler,
                                initial_position=[200, 50],
                                can_be_grabbed=True,
                                deletable=False))

    gui_handler.add_object(StartButton(master=gui_handler,
                                       initial_position=[400, 200]))


def mov_bind():
    return Box, Ball


def menu_scene_loader(gui_handler: GUI):
    menu_scene(gui_handler)
    return mov_bind()
