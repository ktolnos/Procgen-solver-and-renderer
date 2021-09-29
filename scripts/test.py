from bruhai.policy import RandomMovePolicy
from bruhai.rendering import PyGameRenderer
from bruhai.test import Test

if __name__ == "__main__":
    Test(
        policy=RandomMovePolicy(),
        renderer_factory=PyGameRenderer,
        render_n_frame=2,
        runs=10,
    ).run()
