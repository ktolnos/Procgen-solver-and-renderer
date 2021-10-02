import bruhai.utils as utils
from bruhai.keyboard import PyGameKeyboardListener
from bruhai.mastermind import Mastermind
from bruhai.policy import RandomMovePolicy
from bruhai.rendering import PyGameRenderer

if __name__ == "__main__":
    Mastermind(
        policy=RandomMovePolicy(),
        keyboard_listener=PyGameKeyboardListener(),
        renderer_factory=PyGameRenderer,
        sleep_func=utils.pygame_sleep,
    ).run()
