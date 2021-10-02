import bruhai.utils as utils
from bruhai.keyboard import PyGameKeyboardListener
from bruhai.policy import RandomMovePolicy
from bruhai.rendering import PyGameRenderer
from bruhai.test import RunningSpeeds, Test

if __name__ == "__main__":
    Test(
        policy=RandomMovePolicy(),
        keyboard_listener=PyGameKeyboardListener(),
        renderer_factory=PyGameRenderer,
        speed=RunningSpeeds.NORMAL,
        sleep=utils.pygame_sleep,
        runs=10,
    ).run()
