import abc
from dataclasses import dataclass

import numpy as np
import pygame
from numpy import ndarray

TOP_LEFT = (0, 0)


@dataclass
class RendererScreenSettings:
    width: int
    height: int
    scale_factor: int

    def __post_init__(self):
        assert self.width > 0 and self.height > 0 and self.scale_factor > 0
        self.size = self.width, self.height
        self.scaled_size = self.width * self.scale_factor, self.height * self.scale_factor


class Renderer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def render(self, rgb: ndarray) -> bool:
        """Renders the game and handles user input.

        :returns True if environment should continue, False if it should quit.
        """


class PyGameRenderer(Renderer):

    @staticmethod
    def __transform_to_pygame_coordinates(rgb: ndarray):
        transformed_rgb = np.rot90(rgb)
        return np.flip(transformed_rgb, axis=0)

    def __init__(self, screen_settings: RendererScreenSettings):
        pygame.init()
        self.screen_settings = screen_settings
        self.screen = pygame.display.set_mode(screen_settings.scaled_size)
        self.surface = pygame.surface.Surface(screen_settings.size)
        self.scaled_surface = pygame.surface.Surface(screen_settings.scaled_size)
        self.__running = True

    def render(self, rgb: ndarray) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        transformed_rgb = self.__transform_to_pygame_coordinates(rgb)

        pygame.pixelcopy.array_to_surface(self.surface, transformed_rgb)
        pygame.transform.scale(self.surface, self.screen_settings.scaled_size, self.scaled_surface)
        self.screen.blit(self.scaled_surface, TOP_LEFT)
        pygame.display.flip()
        return True
