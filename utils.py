from __future__ import annotations

from enum import Enum
from heapq import heappop, heappush
from math import sqrt
from typing import Tuple, Callable, List, NamedTuple


class MazeLocation(NamedTuple):
    row: int
    column: int


class Colors(Tuple, Enum):
    BLACK = (41, 41, 41)
    WHITE = (245, 245, 245)
    GARY = (220, 220, 220)
    PATH = (119, 214, 140)
    EXPLORE = (121, 119, 214)
    GOAL = (204, 60, 100)
    START = (255, 153, 0)


class PriorityQueue:
    def __init__(self):
        self._container = []

    @property
    def empty(self):
        return not self._container

    def push(self, item) -> None:
        heappush(self._container, item)

    def pop(self) -> any:
        return heappop(self._container)


class Node:
    def __init__(self, location: MazeLocation, parent: Node, cost: int, heuristic: float):
        self.location = location
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(location: MazeLocation):
        return sqrt((goal.row - location.row) ** 2 + (goal.column + location.column) ** 2)

    return distance


def manhattan_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(location: MazeLocation):
        return abs(goal.row - location.row) + abs(goal.column - location.column)

    return distance


def path_to_node(node: Node) -> List[MazeLocation]:
    path: List[MazeLocation] = []
    while node is not None:
        path.append(node.location)
        node = node.parent
    return path[::-1]
