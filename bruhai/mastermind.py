import logging
import time
from typing import Callable, Optional, Type

import gym
import numpy as np
from gym3 import ToGymEnv

from bruhai.keyboard import KeyboardEvent, KeyboardListener
from bruhai.policy import Policy
from bruhai.rendering import Renderer, RendererScreenSettings
from bruhai.running_speed import RunningSpeed

SLEEP_TIME_BETWEEN_GAMES = 0.1

logger = logging.getLogger(__name__)


class Mastermind:
    @staticmethod
    def _add_overlay(obs: np.ndarray, overlay: np.ndarray) -> np.ndarray:
        red, green, blue = overlay[:, :, 0], overlay[:, :, 1], overlay[:, :, 2]
        mask = (red != 0) | (green != 0) | (blue != 0)
        result = np.copy(obs)
        result[mask] = 0
        result += overlay
        return result

    def __init__(
        self,
        policy: Policy,
        keyboard_listener: Optional[KeyboardListener] = None,
        renderer_factory: Optional[Type[Renderer]] = None,
        speed: RunningSpeed = RunningSpeed.Normal,
        runs: int = 10,
        sleep_func: Callable[[float], None] = time.sleep,
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
        self.sleep_func = sleep_func
        self.keyboard_listener = keyboard_listener
        self.is_paused = False
        self.make_step = False
        self.quit = False
        self._set_running_speed(speed)

    def run(self) -> None:
        for episode in range(self.runs):
            self.next_episode()
            if self.quit:
                break
        self.env.close()

    def next_episode(self) -> None:
        self.episode_num += 1
        logger.info(f"Episode #{self.episode_num}")
        self.policy.on_environment_reset()
        obs = self.env.reset()
        step_num = 0
        if self.renderer:
            self.renderer.render(obs)
        reward = 0
        total_reward = 0
        while True:
            if self.keyboard_listener:
                self._listen_keyboard_events()

            if self.quit:
                logger.info(f"Quit on `{step_num}` steps with reward `{total_reward}`.")
                return
            if self.is_paused and not self.make_step:
                continue
            self.make_step = False

            step_num += 1
            action = self.policy.select_action(obs, reward)
            print(f"action {action}")
            log_string = self.policy.debug_info.log
            if log_string:
                logger.debug(log_string)
            obs, reward, done, _ = self.env.step(action)
            total_reward += reward
            if self.renderer and step_num % self.render_n_frame == 0:
                overlay = self.policy.debug_info.overlay
                obs_to_render = obs
                if overlay is not None:
                    obs_to_render = self._add_overlay(obs, overlay)
                self.renderer.render(obs_to_render)
            if self.sleep_between_frames:
                self.sleep_func(self.sleep_between_frames)
            if done:
                break
        logger.info(f"Finished in `{step_num}` steps with reward `{total_reward}`.")
        self.sleep_func(SLEEP_TIME_BETWEEN_GAMES)
        return

    def _listen_keyboard_events(self):
        events = self.keyboard_listener.listen()
        if KeyboardEvent.Quit in events:
            self.quit = True
        if KeyboardEvent.Pause in events:
            self.is_paused = not self.is_paused

        if KeyboardEvent.Step in events:
            self._set_running_speed(RunningSpeed.Step)
        elif KeyboardEvent.SpeedSlow in events:
            self._set_running_speed(RunningSpeed.Slow)
        elif KeyboardEvent.SpeedNormal in events:
            self._set_running_speed(RunningSpeed.Normal)
        elif KeyboardEvent.SpeedFast in events:
            self._set_running_speed(RunningSpeed.Fast)

    def _set_running_speed(self, speed: RunningSpeed):
        self.render_n_frame = speed.value.steps_per_frame
        self.sleep_between_frames = speed.value.sleep_between_frames
        self.is_paused = False
        if speed.value.is_step:
            self.is_paused = True
            self.make_step = True
