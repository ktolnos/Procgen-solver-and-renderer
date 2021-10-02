import bruhai.utils as utils
from bruhai.hardcode_object_recognition import HardCodeObjectRecognition
from bruhai.hardcode_policy import HardCodeMovePolicy
from bruhai.keyboard import PyGameKeyboardListener
from bruhai.mastermind import Mastermind
from bruhai.rendering import PyGameRenderer

if __name__ == "__main__":
    Mastermind(
        policy=HardCodeMovePolicy(HardCodeObjectRecognition()),
        keyboard_listener=PyGameKeyboardListener(),
        renderer_factory=PyGameRenderer,
        sleep_func=utils.pygame_sleep,
    ).run()
