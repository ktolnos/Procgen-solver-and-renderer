from time import sleep
from typing import Callable

import gym
import numpy as np
from gym3 import ToGymEnv

from bruhai.policy import Policy
from bruhai.rendering import Renderer, RendererScreenSettings

SLEEP_TIME_BETWEEN_GAMES = 0.1

RendererFactory = Callable[[RendererScreenSettings], Renderer]


class Test:

    @staticmethod
    def __add_overlay(obs: np.ndarray, overlay: np.ndarray):
        red, green, blue = overlay[:, :, 0], overlay[:, :, 1], overlay[:, :, 2]
        mask = (red != 0) | (green != 0) | (blue != 0)
        obs[mask] = 0
        obs += overlay

    def __init__(
            self,
            policy: Policy,
            renderer_factory: RendererFactory = None,
            render_n_frame: int = 1,
            runs: int = 10
    ):
        self.env: ToGymEnv = gym.make(
            "procgen:procgen-heist-v0",
            use_backgrounds=False,
            use_monochrome_assets=True,
            restrict_themes=True,
        )
        assert render_n_frame > 0
        if renderer_factory:
            self.renderer = renderer_factory(RendererScreenSettings(64, 64, 8))
        self.render_n_frame = render_n_frame
        self.episode_num = 0
        self.policy = policy
        self.runs = runs

    def run(self) -> None:
        for episode in range(self.runs):
            should_continue = self.next_episode()
            if not should_continue:
                break
        self.env.close()

    def next_episode(self) -> bool:
        self.episode_num += 1
        print(f"Episode #{self.episode_num}")
        obs = self.env.reset()
        step_num = 0
        if self.renderer:
            self.renderer.render(obs)
        reward = 0
        total_reward = 0
        while True:
            step_num += 1
            action = self.policy.select_action(obs, reward)
            log_string = self.policy.debug_info.log
            if log_string:
                print(log_string)
            obs, reward, done, _ = self.env.step(action)
            total_reward += reward
            if self.renderer and step_num % self.render_n_frame == 0:
                overlay = self.policy.debug_info.overlay
                if overlay is not None:
                    self.__add_overlay(obs, overlay)
                should_continue = self.renderer.render(obs)
                if not should_continue:
                    print(f"Quit on `{step_num}` steps with reward `{total_reward}`.")
                    return False
            if done:
                break
        print(f"Finished in `{step_num}` steps with reward `{total_reward}`.")
        sleep(SLEEP_TIME_BETWEEN_GAMES)
        return True
