from bruhai.rendering import PyGameRenderer
from bruhai.test import Test

if __name__ == "__main__":
    Test(
        renderer_factory=PyGameRenderer,
        render_n_frame=2,
    ).run()
