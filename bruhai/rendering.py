import abc
from typing import Optional, Tuple

import pygame
from numpy import ndarray


class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def init_display(self, width: int, height: int, scale_factor: int):
        ...

    @abc.abstractmethod
    def render(self, rgb: ndarray):
        ...


class PyGameRenderer(Renderer):
    def __init__(self):
        pygame.init()
        self.size: Optional[Tuple[int, int]] = None
        self.scale_factor: Optional[int] = None
        self.screen: Optional[pygame.Surface] = None

    def init_display(self, width: int, height: int, scale_factor: int):
        assert width > 0 and height > 0 and scale_factor > 0
        self.size = width * scale_factor, height * scale_factor
        self.scale_factor = scale_factor
        self.screen = pygame.display.set_mode(self.size)

    def render(self, rgb: ndarray):
        for x in range(rgb.shape[0]):
            for y in range(rgb.shape[1]):
                for sx in range(self.scale_factor):
                    for sy in range(self.scale_factor):
                        self.screen.set_at(
                            (x * self.scale_factor + sx, y * self.scale_factor + sy),
                            rgb[x, y],
                        )
        pygame.display.flip()
