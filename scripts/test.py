from bruhai.rendering import PyGameRenderer
from bruhai.test import Test

if __name__ == "__main__":
    Test(
        renderer=PyGameRenderer(),
        render_n_frame=16,
    ).run()
