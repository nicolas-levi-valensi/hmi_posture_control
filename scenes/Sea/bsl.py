from utils.hmi_minilib import GUI
from scenes.Sea.objects import Fish0, Fish1, Fish2, Shell0, Shell1, Shark0, Shark1


def base_scene(gui_handler: GUI) -> None:
    gui_handler.set_background(path="Assets/sprites/Sea/bg_underwater.jpg")

    gui_handler.add_object(Shark0(master=gui_handler,
                                  initial_position=[400, 150],
                                  can_be_grabbed=True,
                                  deletable=True))

    gui_handler.add_object(Shark1(master=gui_handler,
                                  initial_position=[110, 70],
                                  can_be_grabbed=True,
                                  deletable=True))

    gui_handler.add_object(Fish0(master=gui_handler,
                                 initial_position=[150, 250],
                                 can_be_grabbed=True,
                                 deletable=True))

    gui_handler.add_object(Fish1(master=gui_handler,
                                 initial_position=[550, 80],
                                 can_be_grabbed=True,
                                 deletable=True))

    gui_handler.add_object(Fish2(master=gui_handler,
                                 initial_position=[440, 300],
                                 can_be_grabbed=True,
                                 deletable=True))

    gui_handler.add_object(Shell1(master=gui_handler,
                                  initial_position=[190, 420],
                                  can_be_grabbed=True,
                                  deletable=False))

    gui_handler.add_object(Shell0(master=gui_handler,
                                  initial_position=[350, 390],
                                  can_be_grabbed=True,
                                  deletable=False))


def mov_bind():
    return Fish2, Fish1


def fish_scene_loader(gui_handler: GUI):
    base_scene(gui_handler)
    return mov_bind()
