from __future__ import annotations
import os
import signal
import numpy as np
import cv2
from colorama import Fore, Style, Back
from tabulate import tabulate

from nico_lib.hvc_minilib import HandVideoClassifier
from nico_lib.hmi_minilib import Ball, Box, GUI, Text, Fish1, Fish2, Shell1, Shell2

# ------------- EXECUTION SETTINGS -----------
SHOW_INFO_AT_STARTUP = True

MODEL_PATH = "Assets/model_data/model.h5"  # TensorFlow Keras model path root
DATA_PATH = "Assets/datasets_records"  # The data path is used to extract the list of labels
USE_VERBOSE_ON_HVC = True  # Enables INFO output from HandVideoClassifier
VIDEO_OUTPUT = True  # Enables the video output of the camera (optional)

# -------------- Data formatting --------------
MODEL_OUTPUT_LABELS = [class_file[:-4] for class_file in os.listdir(DATA_PATH)]
POSTURE_DICT = dict(zip(MODEL_OUTPUT_LABELS, range(len(MODEL_OUTPUT_LABELS))))

# -------------- USAGE SETTINGS ---------------
# Use POSTURE_DICT["name_of_the_csv_file"] or the direct output index of the model
GRAB_INDEX = POSTURE_DICT["closed_hand"]
ADD_BALL_INDEX = POSTURE_DICT["up"]
ADD_BOX_INDEX = POSTURE_DICT["thumb_up"]
DEL_INDEX = POSTURE_DICT["pinch"]


def create_base_scene(gui_handler: GUI) -> None:
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

    fish = Fish1(master=gui_handler,
                 initial_position=[200, 200],
                 can_be_grabbed=True,
                 deletable=False)
    gui_handler.add_object(fish)


def create_fish_scene(gui_handler: GUI) -> None:
    gui_handler.set_background(path="./Assets/sprites/bg_underwater.jpg")

    gui_handler.add_object(Fish1(master=gui_handler,
                                 initial_position=[400, 200],
                                 can_be_grabbed=True,
                                 deletable=False))

    gui_handler.add_object(Fish1(master=gui_handler,
                                 initial_position=[500, 270],
                                 can_be_grabbed=True,
                                 deletable=False))

    gui_handler.add_object(Fish2(master=gui_handler,
                                 initial_position=[100, 150],
                                 can_be_grabbed=True,
                                 deletable=False))

    gui_handler.add_object(Fish2(master=gui_handler,
                                 initial_position=[200, 280],
                                 can_be_grabbed=True,
                                 deletable=False))

    gui_handler.add_object(Shell1(master=gui_handler,
                                  initial_position=[190, 420],
                                  can_be_grabbed=True,
                                  deletable=False))

    gui_handler.add_object(Shell2(master=gui_handler,
                                  initial_position=[350, 390],
                                  can_be_grabbed=True,
                                  deletable=False))


INITIAL_SCENE = create_fish_scene


def main() -> None:
    # Video capture and detection initialisation
    hvc = HandVideoClassifier(model_path=MODEL_PATH, stream_path=0, video_output=VIDEO_OUTPUT,
                              labels_on_vid=MODEL_OUTPUT_LABELS, verbose=USE_VERBOSE_ON_HVC).start()

    # Graphic interface initialisation
    hmi = GUI(window_name="Interface")

    # Ctrl-C handling for clean subprocess shutdown
    signal.signal(signal.SIGINT, hvc.stop)

    if INITIAL_SCENE is not None:
        INITIAL_SCENE(gui_handler=hmi)

    prev_states = [-1, -1]  # Stores the previous hand states to detect changes in hands postures
    while hvc.is_running():  # Mainloop tests and actions
        states = hvc.get_predictions()
        hands_coords = hvc.get__hands_coords()
        hmi.set_hands_coords(hands_coords)

        # Grab test
        for hand_pos, hand_id in zip(hands_coords, range(2)):
            for obj in hmi.objects:
                held = False
                if (np.less(np.abs(np.subtract(obj.get_position(), hand_pos)), obj.get_hit_box())).all() \
                        and states[hand_id] == GRAB_INDEX and prev_states[hand_id] != GRAB_INDEX:
                    obj.set_grabbed(grabbed=True, holder_index=hand_id)
                    held = True
                elif obj.is_grabbed() and hand_id == obj.grabbed_by and states[hand_id] == GRAB_INDEX:
                    obj.set_position(position=hand_pos)
                    held = True
                if not held and hand_id == obj.grabbed_by:
                    obj.set_grabbed(grabbed=False)
                elif held:
                    break

        # Object deletion
        for hand_pos, hand_id in zip(hands_coords, range(2)):
            for obj, obj_id in zip(hmi.objects, range(len(hmi.objects))):
                if (np.less(np.abs(np.subtract(obj.get_position(), hand_pos)), obj.get_hit_box())).all() \
                        and states[hand_id] == DEL_INDEX and prev_states[hand_id] != DEL_INDEX:
                    hmi.delete_object(obj_id)
                    break

        # Adding balls on hand position if ADD_BALL_INDEX state is reached by hand
        for state, prev_state, xy in zip(states, prev_states, hands_coords):
            if state == ADD_BALL_INDEX and prev_state != ADD_BALL_INDEX:
                hmi.add_object(Ball(master=hmi, initial_position=xy, ball_radius=20, color=np.random.random(size=3)))

        # Adding boxes on hand position if ADD_BOX_INDEX state is reached by hand
        for state, prev_state, xy in zip(states, prev_states, hands_coords):
            if state == ADD_BOX_INDEX and prev_state != ADD_BOX_INDEX:
                hmi.add_object(Box(master=hmi, initial_position=xy, box_size=[40, 50], color=np.random.random(size=3)))

        prev_states = states

        hmi.draw()
        if cv2.waitKey(1) == 27:
            if hvc.is_running():  # If ended by Ctrl-C, the process could have stopped the hvc before
                hvc.stop()
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    if SHOW_INFO_AT_STARTUP:
        print("\n")
        print(Fore.BLUE + Back.WHITE + f"INFO: THIS SCRIPT CAN BE CONFIGURED AT THE BEGINNING OF THE FILE")
        print(Style.RESET_ALL + "(Config. and classes infos can be disabled by setting SHOW_INFO_AT_STARTUP = False)\n")
        print(Fore.LIGHTBLUE_EX + "CONFIGURATION :\n\n" +
              tabulate(tabular_data=[["MODEL_PATH", MODEL_PATH],
                                     ["DATA_PATH", DATA_PATH],
                                     ["USE_VERBOSE_ON_HVC", USE_VERBOSE_ON_HVC],
                                     ["VIDEO_OUTPUT", VIDEO_OUTPUT]],
                       headers=["PARAMS", "VALUE"],
                       tablefmt="github",
                       stralign="left"))
        print(Style.RESET_ALL)
        print(Fore.LIGHTBLUE_EX + "\nDETECTED CLASSES :\n\n" +
              tabulate(tabular_data=zip(POSTURE_DICT.values(), POSTURE_DICT.keys()),
                       headers=["OUT", "LABEL"],
                       tablefmt="github",
                       stralign="left",
                       numalign="left") + "\n\n")
    main()
