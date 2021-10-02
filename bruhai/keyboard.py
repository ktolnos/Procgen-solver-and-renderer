from enum import IntEnum
from typing import Set

import pygame


class KeyboardActions(IntEnum):
    QUIT = 0
    PAUSE = 1
    STEP = 2
    SPEED_FAST = 3
    SPEED_NORMAL = 4
    SPEED_SLOW = 5


class KeyboardListener:
    actions: Set[KeyboardActions]


class PyGameKeyboardListener(KeyboardListener):

    @property
    def actions(self):
        actions_set = set()
        for event in pygame.event.get(pygame.KEYDOWN):
            if event.key == pygame.K_p:
                actions_set.add(KeyboardActions.PAUSE)
            if event.key == pygame.K_s:
                actions_set.add(KeyboardActions.STEP)
            if event.key == pygame.K_1:
                actions_set.add(KeyboardActions.SPEED_SLOW)
            if event.key == pygame.K_2:
                actions_set.add(KeyboardActions.SPEED_NORMAL)
            if event.key == pygame.K_3:
                actions_set.add(KeyboardActions.SPEED_FAST)
        if pygame.event.get(pygame.QUIT):
            actions_set.add(KeyboardActions.QUIT)
        return actions_set
