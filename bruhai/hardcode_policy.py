import random
from typing import Set

import numpy as np

from bruhai.hardcode_object_recognition import (Entities,
                                                HardCodeObjectRecognition)
from bruhai.pathfinding import AStar
from bruhai.policy import MOVE_ACTIONS, Actions, Policy
from bruhai.utils import Point

all_entities = {x.value for x in Entities}
colliders = {Entities.DOOR1.value, Entities.DOOR2.value, Entities.DOOR3.value, Entities.WALL}
initial_triggers = all_entities - colliders

key_to_collected_pos = {
    Entities.KEY1: Point(3, 61),
    Entities.KEY2: Point(3, 57),
    Entities.KEY3: Point(3, 53),
}


class HardCodeMovePolicy(Policy):
    last_player_pos: Point
    triggers: Set[Entities]

    def __init__(self, object_recognition: HardCodeObjectRecognition):
        super().__init__()
        self.object_recognition = object_recognition
        self.on_environment_reset()

    def on_environment_reset(self):
        self.last_player_pos = Point(-1, -1)
        self.triggers = initial_triggers.copy()

    def select_action(self, observation: np.ndarray, last_reward: int) -> int:
        self.debug_info.overlay = np.zeros_like(observation)

        entity_obs = self.object_recognition.recognize(observation)

        player_pos = self.object_recognition.recognized_objects[Entities.PLAYER].position
        self.debug_info.overlay[player_pos.x, player_pos.y] = np.array([255, 0, 0])
        if player_pos == self.last_player_pos:
            return random.choice(MOVE_ACTIONS)
        self.last_player_pos = player_pos

        self.update_triggers()

        target_entity = self.get_target()
        target_pos = self.object_recognition.recognized_objects[target_entity].position
        self.debug_info.overlay[target_pos.x, target_pos.y] = np.array([0, 0, 255])

        grid = np.zeros_like(entity_obs)
        for entity in self.triggers:
            grid |= entity_obs == entity

        path = AStar(grid, player_pos, target_pos, offset=1).run()

        if not path:
            return random.choice(MOVE_ACTIONS)

        first_non_player = path[-1]
        last_player = path[0]
        path.reverse()
        found_first_non_player = False

        for (l, node) in enumerate(path):
            if entity_obs[node.x, node.y] != Entities.PLAYER.value and not found_first_non_player:
                first_non_player = node
                found_first_non_player = True
            if entity_obs[node.x, node.y] == Entities.PLAYER.value:
                last_player = node
            self.debug_info.overlay[node.x, node.y] = np.array([0, 255, int((l / len(path)) * 255)])

        dir_x = first_non_player.x - last_player.x
        dir_y = first_non_player.y - last_player.y
        if dir_x > 0:
            return Actions.RIGHT
        if dir_x < 0:
            return Actions.LEFT
        if dir_y > 0:
            return Actions.DOWN
        return Actions.UP

    def get_target(self):
        recognized_objects = self.object_recognition.recognized_objects

        if self.has_uncollected_key(Entities.KEY1):
            return Entities.KEY1
        if Entities.DOOR1 in recognized_objects:
            return Entities.DOOR1
        if self.has_uncollected_key(Entities.KEY2):
            return Entities.KEY2
        if Entities.DOOR2 in recognized_objects:
            return Entities.DOOR2
        if self.has_uncollected_key(Entities.KEY3):
            return Entities.KEY3
        if Entities.DOOR3 in recognized_objects:
            return Entities.DOOR3
        return Entities.TARGET

    def update_triggers(self):
        if self.has_collected_key(Entities.KEY1):
            self.triggers.add(Entities.DOOR1.value)
        if self.has_collected_key(Entities.KEY2):
            self.triggers.add(Entities.DOOR2.value)
        if self.has_collected_key(Entities.KEY3):
            self.triggers.add(Entities.DOOR3.value)

    def has_collected_key(self, key: Entities):
        if key not in self.object_recognition.recognized_objects:
            return False
        rec = self.object_recognition.recognized_objects[key]
        return rec.position == key_to_collected_pos[key]

    def has_uncollected_key(self, key: Entities):
        if key not in self.object_recognition.recognized_objects:
            return False
        rec = self.object_recognition.recognized_objects[key]
        return rec.position != key_to_collected_pos[key]
