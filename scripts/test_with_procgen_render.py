from procgen import ProcgenGym3Env
import gym3
import numpy as np
from numpy.random import default_rng

from enum import IntEnum


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


def main():
    rng = default_rng()
    env = ProcgenGym3Env(
        num=1,
        env_name="heist",
        use_backgrounds=False,
        use_monochrome_assets=True,
        restrict_themes=True,
    )
    print(env.ac_space)
    env = gym3.ViewerWrapper(env, ob_key="rgb", tps=100)
    step = 0
    np_move_actions = np.array(MOVE_ACTIONS)
    action = np.array([0], dtype=np.int32)
    while True:
        action[0] = rng.choice(np_move_actions)
        env.act(action)
        rew, obs, is_first_frame = env.observe()
        if step % 10 == 0:
            print(f"Step = ${step}, Reward = {rew}")
        step += 1


if __name__ == "__main__":
    main()
