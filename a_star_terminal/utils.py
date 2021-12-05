from __future__ import annotations

from enum import Enum
from heapq import heappop, heappush
from math import sqrt
from typing import NamedTuple, Callable


class Cell(str, Enum):
    BLOCK = "#"
    START = "S"
    GOAL = "G"
    PATH = "*"
    EMPTY = " "


class Location(NamedTuple):
    row: int
    column: int


class Node:
    def __init__(self, location: Location, parent: Node, cost: int, heuristic: float):
        """
        Initialize for Node
        :param location: where the node locate in the maze
        :param parent: the previous location
        :param cost: the actual cost from the start to this location
        :param heuristic: the heuristic value to reach the goal
        """
        self.location = location
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other: Node):
        """
        This method will be used by the priority queue to determine the lower value
        :param other
        :return: bool
        """
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class PriorityQueue:
    """
    We will use the built-in implementation of for adding Node, and pulling Node from list
    """

    def __init__(self):
        """
        Initialize the list
        """
        self._list = []

    @property
    def empty(self):
        """Checking property if the list is empty"""
        return not self._list

    def push(self, node: Node):
        """
        Adding element using heappush method from python
        :param node: Node
        """
        heappush(self._list, node)

    def pop(self) -> Node:
        """
        Return the lower value in the list using the heappop from python
        :return: Node
        """
        return heappop(self._list)


def euclidean_distance(goal: Location) -> Callable[[Location], float]:
    def distance(location: Location):
        return sqrt((goal.row - location.row) ** 2 + (goal.column - location.column) ** 2)

    return distance


def manhattan_distance(goal: Location) -> Callable[[Location], float]:
    def distance(location: Location):
        return abs(goal.row - location.row) + abs(goal.column - location.column)

    return distance


def chebyshev_distance(goal: Location) -> Callable[[Location], float]:
    def distance(location: Location):
        dx = abs(goal.row - location.row)
        dy = abs(goal.column - location.column)
        return max(dx, dy)

    return distance


def path_to_node(node: Node):
    path = []
    while node is not None:
        path.append(node.location)
        node = node.parent
    return path[::-1]
