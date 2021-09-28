import abc

import pygame
from numpy import ndarray


class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self, width: int, height: int, scale_factor: int):
        ...

    @abc.abstractmethod
    def render(self, rgb: ndarray) -> None:
        ...


class PyGameRenderer(Renderer):
    def __init__(self, width: int, height: int, scale_factor: int):
        assert width > 0 and height > 0 and scale_factor > 0
        pygame.init()
        self.size = width * scale_factor, height * scale_factor
        self.scale_factor = scale_factor
        self.screen = pygame.display.set_mode(self.size)

    def render(self, rgb: ndarray) -> None:
        for x in range(rgb.shape[0]):
            for y in range(rgb.shape[1]):
                for sx in range(self.scale_factor):
                    for sy in range(self.scale_factor):
                        self.screen.set_at(
                            (x * self.scale_factor + sx, y * self.scale_factor + sy),
                            rgb[x, y],
                        )
        pygame.display.flip()
