import heapq
from dataclasses import dataclass
from typing import Any, List, Tuple

import pygame


def pygame_sleep(seconds: float) -> None:
    pygame.time.wait(int(seconds * 1000))


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __lt__(self, other):
        return self.x < other.x


@dataclass(frozen=True)
class Rect:
    left: int
    top: int
    right: int
    bottom: int


class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[int, Any]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: Any, priority: int):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> Any:
        return heapq.heappop(self.elements)[1]
