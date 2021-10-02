from dataclasses import dataclass
from enum import IntEnum
from typing import Dict

import numpy as np

from bruhai.utils import Point, Rect


class Entities(IntEnum):
    BG = 0
    WALL = 1
    PLAYER = 2
    TARGET = 3
    DOOR1 = 4
    DOOR2 = 5
    DOOR3 = 6
    KEY1 = 7
    KEY2 = 8
    KEY3 = 9


all_entities = {x.value for x in Entities}
objects = all_entities - {Entities.WALL, Entities.BG}


def r_g_b_to_color_int(r: int, g: int, b: int) -> int:
    return r + 255 * g + 255 * 255 * b


@dataclass
class RecognizedObject:
    type: int
    position: Point
    rect: Rect

    @property
    def size(self) -> Rect:
        return Rect(
            self.rect.left - self.position.x,
            self.rect.top - self.position.y,
            self.rect.right - self.position.x,
            self.rect.bottom - self.position.y,
        )


class HardCodeObjectRecognition:
    __color_to_entity = {
        r_g_b_to_color_int(0, 0, 0): Entities.BG,
        r_g_b_to_color_int(191, 127, 63): Entities.WALL,
        r_g_b_to_color_int(127, 255, 127): Entities.PLAYER,
        r_g_b_to_color_int(191, 63, 191): Entities.TARGET,
        r_g_b_to_color_int(255, 191, 191): Entities.DOOR1,
        r_g_b_to_color_int(63, 255, 127): Entities.DOOR2,
        r_g_b_to_color_int(191, 63, 63): Entities.DOOR3,
        r_g_b_to_color_int(127, 127, 255): Entities.KEY1,
        r_g_b_to_color_int(191, 191, 191): Entities.KEY2,
        r_g_b_to_color_int(255, 255, 127): Entities.KEY3,
    }

    recognized_objects: Dict[Entities, RecognizedObject] = {}

    def recognize(self, obs: np.ndarray) -> np.ndarray:
        self.recognized_objects.clear()

        obs = obs.astype(np.int32)
        r, g, b = obs[:, :, 0], obs[:, :, 1], obs[:, :, 2]
        color_int_obs = r + (g * 255) + (b * 255 * 255)
        for color, entity in self.__color_to_entity.items():
            mask = color_int_obs == color
            color_int_obs[mask] = entity.value
            if entity not in objects:
                continue
            indices = np.nonzero(mask)
            if not indices or indices[0].size == 0 or indices[1].size == 0:
                continue
            x_first, x_last = indices[0][0], indices[0][-1]
            y_first, y_last = indices[1][0], indices[1][-1]
            pos_x = (x_first + x_last) // 2
            pos_y = (y_first + y_last) // 2

            obj = RecognizedObject(
                type=entity,
                position=Point(pos_x, pos_y),
                rect=Rect(x_first, y_first, x_last, y_last)
            )

            self.recognized_objects[entity] = obj
        return color_int_obs
