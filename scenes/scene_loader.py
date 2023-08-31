import numpy as np
from utils.hmi_minilib import GUI
from utils.hvc_minilib import HandVideoClassifier
import cv2

# Scenes loaders
from scenes.default.bsl import default_scene_loader
from scenes.Sea.bsl import fish_scene_loader
from scenes.Space.bsl import space_scene_loader
from scenes.Town.bsl import town_scene_loader
from scenes.Menu.bsl import menu_scene_loader

SCENES = {"menu": menu_scene_loader,
          "sea": fish_scene_loader,
          "space": space_scene_loader,
          "town": town_scene_loader,
          "default": default_scene_loader}


def load_scene(scene_name: str, gui_handler: GUI):
    for index, element in enumerate(gui_handler.objects):
        gui_handler.delete_object(index)

    if scene_name.lower() in SCENES.keys():
        return SCENES[scene_name.lower()](gui_handler)
    else:
        raise ValueError(f'Scene "{scene_name.lower()}" doesnt exist, '
                         f'please select between {[key for key in SCENES.keys()]}')


def menu_behavior(hvc: HandVideoClassifier, hmi: GUI,
                  grab_index: int, del_index: int, add_obj1_ind: int, add_obj2_ind: int):
    obj1, obj2 = load_scene("menu", hmi)

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
                        and states[hand_id] == grab_index and prev_states[hand_id] != grab_index:
                    obj.set_grabbed(grabbed=True, holder_index=hand_id)
                    held = True
                elif obj.is_grabbed() and hand_id == obj.grabbed_by and states[hand_id] == grab_index:
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
                        and states[hand_id] == del_index and prev_states[hand_id] != del_index:
                    obj.click()
                    break

        # Adding balls on hand position if ADD_OBJ1_IND state is reached by hand
        for state, prev_state, xy in zip(states, prev_states, hands_coords):
            if state == add_obj1_ind and prev_state != add_obj1_ind:
                hmi.add_object(obj1(master=hmi, initial_position=xy))

        # Adding boxes on hand position if ADD_OBJ2_IND state is reached by hand
        for state, prev_state, xy in zip(states, prev_states, hands_coords):
            if state == add_obj2_ind and prev_state != add_obj2_ind:
                hmi.add_object(obj2(master=hmi, initial_position=xy))

        prev_states = states

        hmi.draw()
        if cv2.waitKey(1) == 27:
            if hvc.is_running():  # If ended by Ctrl-C, the process could have stopped the hvc before
                hvc.stop()
            break


if __name__ == '__main__':
    raise Exception("This file isn't meant to be executed.")
