import random
from enum import IntEnum
from time import sleep
from typing import Type, Optional

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
    def __init__(self, renderer_class: Type[Renderer] = None, render_n_frame: int = 1):
        self.env: ToGymEnv = gym.make("procgen:procgen-heist-v0")
        assert render_n_frame > 0
        self.renderer: Optional[Renderer] = renderer_class(64, 64, 8) if renderer_class else None
        self.render_n_frame = render_n_frame
        self.episode_num = 0

    def run(self) -> None:
        for episode in range(10):
            self.next_episode()
        self.env.close()

    def next_episode(self) -> None:
        self.episode_num += 1
        print(f"Episode #{self.episode_num}")
        obs = self.env.reset()
        step_num = 0
        if self.renderer:
            self.renderer.render(obs)
        sleep(1)
        reward = 0
        while True:
            rand_action = random.choice(MOVE_ACTIONS)
            nobs, reward, done, _ = self.env.step(rand_action)
            if self.renderer and step_num % self.render_n_frame == 0:
                self.renderer.render(nobs)
            if done:
                break
            step_num += 1
        print(f"Finished in `{step_num}` steps with reward `{reward}`.")
        sleep(1)
