import pygame


def pygame_sleep(seconds: float) -> None:
    pygame.time.wait(int(seconds * 1000))
