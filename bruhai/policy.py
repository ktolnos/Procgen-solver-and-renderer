import abc
import random
from enum import IntEnum
from typing import Optional

import numpy as np


class Actions(IntEnum):
    UP_RIGHT = 0
    UP = 1
    UP_LEFT = 2
    RIGHT = 3
    STAY = 4
    LEFT = 5
    DOWN_RIGHT = 6
    DOWN = 7
    DOWN_LEFT = 8


MOVE_ACTIONS = (
    Actions.UP,
    Actions.UP_RIGHT,
    Actions.RIGHT,
    Actions.DOWN_RIGHT,
    Actions.DOWN,
    Actions.DOWN_LEFT,
    Actions.LEFT,
    Actions.UP_LEFT,
)


class PolicyDebugInfo:
    """Overlay to draw over next observation"""
    overlay: Optional[np.ndarray] = None
    log: str = ""


class Policy(metaclass=abc.ABCMeta):
    def __init__(self):
        self.debug_info: PolicyDebugInfo = PolicyDebugInfo()

    @abc.abstractmethod
    def select_action(self, observation: np.ndarray, last_reward: int) -> int:
        ...


class RandomMovePolicy(Policy):
    def select_action(self, observation: np.ndarray, last_reward: int) -> int:
        return random.choice(MOVE_ACTIONS)
