from __future__ import annotations
import os
import signal
import numpy as np
import cv2
from colorama import Fore, Style, Back
from tabulate import tabulate

from utils.hvc_minilib import HandVideoClassifier
from utils.hmi_minilib import GUI
from scenes.scene_loader import load_scene

# ------------- EXECUTION SETTINGS -----------
SHOW_INFO_AT_STARTUP = True
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

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
ADD_OBJ1_IND = POSTURE_DICT["up"]
ADD_OBJ2_IND = POSTURE_DICT["thumb_up"]
DEL_INDEX = POSTURE_DICT["pinch"]
CLICK_INDEX = POSTURE_DICT["rock"]

SCENE_TO_LOAD = "space"


def main() -> None:
    # Video capture and detection initialisation
    hvc = HandVideoClassifier(model_path=MODEL_PATH, stream_path=0, video_output=VIDEO_OUTPUT,
                              labels_on_vid=MODEL_OUTPUT_LABELS, verbose=USE_VERBOSE_ON_HVC).start()

    # Graphic interface initialisation
    hmi = GUI(window_name="Interface")

    # Ctrl-C handling for clean subprocess shutdown
    signal.signal(signal.SIGINT, hvc.stop)

    # TODO: Add menu

    finger_objects = load_scene(SCENE_TO_LOAD, hmi)

    loaded_scene = SCENE_TO_LOAD
    prev_states = [-1, -1]  # Stores the previous hand states to detect changes in hands postures
    while hvc.is_running():  # Mainloop tests and actions
        if SCENE_TO_LOAD == loaded_scene:
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
                for obj_id, obj in enumerate(hmi.objects):
                    if (np.less(np.abs(np.subtract(obj.get_position(), hand_pos)), obj.get_hit_box())).all() \
                            and states[hand_id] == DEL_INDEX and prev_states[hand_id] != DEL_INDEX:
                        hmi.delete_object(obj_id)
                        break

            # Object deletion
            for hand_pos, hand_id in zip(hands_coords, range(2)):
                for obj_id, obj in enumerate(hmi.objects):
                    if (np.less(np.abs(np.subtract(obj.get_position(), hand_pos)), obj.get_hit_box())).all() \
                            and states[hand_id] == CLICK_INDEX and prev_states[hand_id] != CLICK_INDEX:
                        obj.click()
                        break

            for posture_ind, obj in zip([ADD_OBJ1_IND, ADD_OBJ2_IND], finger_objects):
                # Adding OBJ on hand position if ADD_OBJ2_IND state is reached by hand
                for state, prev_state, xy in zip(states, prev_states, hands_coords):
                    if state == posture_ind and prev_state != posture_ind:
                        hmi.add_object(obj(master=hmi, initial_position=xy))

            prev_states = states

            hmi.draw()
            if cv2.waitKey(1) == 27:
                if hvc.is_running():  # If ended by Ctrl-C, the process could have stopped the hvc before
                    hvc.stop()
                break
        else:
            finger_objects = load_scene(SCENE_TO_LOAD, hmi)

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
