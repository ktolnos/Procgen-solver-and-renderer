import random
from enum import IntEnum
from time import sleep
from typing import Optional

import gym
from gym3 import ToGymEnv

from bruhai.rendering import Renderer


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


class Test:
    def __init__(self, renderer: Renderer = None, render_n_frame: int = 1):
        assert render_n_frame > 0
        self.env: Optional[ToGymEnv] = None
        self.renderer = renderer
        self.render_n_frame = render_n_frame
        self.episode_num = 0
        self.step_num = 0

    def run(self):
        self.env = gym.make("procgen:procgen-heist-v0")
        print(type(self.env))
        for episode in range(1):
            self.next_episode()
        self.env.close()

    def next_episode(self):
        self.episode_num += 1
        print(f"Episode #{self.episode_num}")
        obs = self.env.reset()
        self.step_num = 0
        if self.renderer:
            self.renderer.init_display(64, 64, 8)
            self.renderer.render(obs)
        sleep(1)
        while True:
            rand_action = random.choice(MOVE_ACTIONS)
            nobs, reward, done, _ = self.env.step(rand_action)
            if self.renderer and self.step_num % self.render_n_frame == 0:
                self.renderer.render(nobs)
            if done:
                break
            self.step_num += 1
        print(self.step_num)
        sleep(1)
