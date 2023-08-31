from utils.hmi_minilib import GUI, Box, Ball, Text


def base_scene(gui_handler: GUI) -> None:
    """
    Base scene example to generate a few object.
    :param gui_handler: GUI object from hmi_minilib
    :type gui_handler: GUI
    """
    # Scene initialisation (example)
    box_0 = Box(master=gui_handler,
                initial_position=[200, 200],
                box_size=[40, 30],
                color=(0.1, 0.8, 0))
    gui_handler.add_object(box_0)

    box_1 = Box(master=gui_handler,
                initial_position=[300, 100],
                box_size=[80, 60],
                color=(0, 0.3, 0.7))
    gui_handler.add_object(box_1)

    ball_0 = Ball(master=gui_handler,
                  initial_position=[400, 400],
                  ball_radius=30,
                  color=(0.1, 0.2, 0.3))
    gui_handler.add_object(ball_0)

    text_0 = Text(master=gui_handler,
                  initial_position=[300, 60],
                  text="Deletable text",
                  font_size=1,
                  color=(0.8, 0.2, 0.8),
                  deletable=True)
    gui_handler.add_object(text_0)

    text_1 = Text(master=gui_handler,
                  initial_position=[200, 360],
                  text="Not deletable",
                  font_size=1,
                  color=(0.4, 0.2, 0.9),
                  deletable=False)
    gui_handler.add_object(text_1)

    text_2 = Text(master=gui_handler,
                  initial_position=[130, 40],
                  text="Pinch to delete",
                  font_size=1,
                  color=(0.9, 0.9, 0.4),
                  deletable=False)
    gui_handler.add_object(text_2)

    text_3 = Text(master=gui_handler,
                  initial_position=[150, 120],
                  text="Grab to displace",
                  font_size=1,
                  color=(0.9, 0.5, 0.5),
                  deletable=False)
    gui_handler.add_object(text_3)

    text_4 = Text(master=gui_handler,
                  initial_position=[350, 220],
                  text="Fixed text",
                  font_size=1,
                  color=(0.9, 0.5, 0.5),
                  deletable=False,
                  can_be_grabbed=False)
    gui_handler.add_object(text_4)


def mov_bind():
    return Box, Ball


def default_scene_loader(gui_handler: GUI):
    base_scene(gui_handler)
    return mov_bind()
