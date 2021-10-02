import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

import gym
import numpy as np
from gym3 import ToGymEnv

from bruhai.keyboard import KeyboardActions, KeyboardListener
from bruhai.policy import Policy
from bruhai.rendering import Renderer, RendererScreenSettings

SLEEP_TIME_BETWEEN_GAMES = 0.1
NORMAL_SPEED_STEPS_PER_FRAME = 1
FAST_SPEED_STEPS_PER_FRAME = 8
SLOW_SPEED_INTER_FRAME_DELAY = 0.5

RendererFactory = Callable[[RendererScreenSettings], Renderer]


@dataclass(eq=False)
class RunningSpeed:
    steps_per_frame: int
    sleep_between_frames: Optional[float] = None


class RunningSpeeds(Enum):
    SLOW = RunningSpeed(1, SLOW_SPEED_INTER_FRAME_DELAY)
    NORMAL = RunningSpeed(NORMAL_SPEED_STEPS_PER_FRAME)
    FAST = RunningSpeed(FAST_SPEED_STEPS_PER_FRAME)
    STEP = RunningSpeed(1)


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
            keyboard_listener: Optional[KeyboardListener] = None,
            renderer_factory: Optional[RendererFactory] = None,
            speed: RunningSpeeds = RunningSpeeds.NORMAL,
            runs: int = 10,
            sleep: Callable[[float], None] = time.sleep,
    ):
        self.env: ToGymEnv = gym.make(
            "procgen:procgen-heist-v0",
            use_backgrounds=False,
            use_monochrome_assets=True,
            restrict_themes=True,
        )
        if renderer_factory:
            self.renderer = renderer_factory(RendererScreenSettings(64, 64, 8))
        self.episode_num = 0
        self.policy = policy
        self.runs = runs
        self.sleep = sleep
        self.keyboard_listener = keyboard_listener
        self.is_paused = False
        self.make_step = False
        self.quit = False
        self.__set_running_speed(speed)

    def run(self) -> None:
        for episode in range(self.runs):
            self.next_episode()
            if self.quit:
                break
        self.env.close()

    def next_episode(self) -> None:
        self.episode_num += 1
        print(f"Episode #{self.episode_num}")
        obs = self.env.reset()
        step_num = 0
        if self.renderer:
            self.renderer.render(obs)
        reward = 0
        total_reward = 0
        while True:
            self.__handle_keyboard_input_if_needed()

            if self.quit:
                print(f"Quit on `{step_num}` steps with reward `{total_reward}`.")
                return
            if self.is_paused and not self.make_step:
                continue
            self.make_step = False

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
                self.renderer.render(obs)
            if self.sleep_between_frames:
                self.sleep(self.sleep_between_frames)
            if done:
                break
        print(f"Finished in `{step_num}` steps with reward `{total_reward}`.")
        self.sleep(SLEEP_TIME_BETWEEN_GAMES)
        return

    def __handle_keyboard_input_if_needed(self):
        if self.keyboard_listener is None:
            return
        actions = self.keyboard_listener.actions
        if KeyboardActions.QUIT in actions:
            self.quit = True
        if KeyboardActions.PAUSE in actions:
            self.is_paused = not self.is_paused
        if KeyboardActions.STEP in actions:
            self.__set_running_speed(RunningSpeeds.STEP)
        if KeyboardActions.SPEED_SLOW in actions:
            self.__set_running_speed(RunningSpeeds.SLOW)
        if KeyboardActions.SPEED_NORMAL in actions:
            self.__set_running_speed(RunningSpeeds.NORMAL)
        if KeyboardActions.SPEED_FAST in actions:
            self.__set_running_speed(RunningSpeeds.FAST)

    def __set_running_speed(self, speed: RunningSpeeds):
        self.render_n_frame = speed.value.steps_per_frame
        self.sleep_between_frames = speed.value.sleep_between_frames
        self.is_paused = False
        if speed is RunningSpeeds.STEP:
            self.is_paused = True
            self.make_step = True
