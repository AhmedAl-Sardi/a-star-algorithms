import time
from typing import Dict, List, Union, Callable

import pygame

from maze import Maze
from utils import (PriorityQueue, Node,
                   path_to_node,
                   Location, Cell)


class AStar:
    def __init__(self, heuristic: Callable[[Location], float],
                 successor: Callable[[Location, bool], List[Location]],
                 goal_check: Callable[[Location], bool],
                 start: Location, maze: Maze,
                 allow_diagonal: bool):
        self._heuristic: Callable[[Location], float] = heuristic
        self._successor = successor
        self._goal_check = goal_check
        self._start = start
        self._maze: Maze = maze
        self._solution: Union[Node, None] = None
        self._time: float = 0.0
        self._len_of_path: int = 0
        self._allow_diagonal = allow_diagonal

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, heuristic):
        self._heuristic = heuristic

    def start(self):
        t1 = time.perf_counter()
        self._solution: Node = self._search()
        t2 = time.perf_counter()
        self._time = t2 - t1
        print(f"time to take: {t2 - t1}")

        if not self._solution:
            print("No solution found")
            return
        paths: List[Location] = path_to_node(self._solution)
        self._len_of_path = len(paths)
        for location in paths:
            self._maze.mark(location=location, color=Cell.PATH)
            self._maze.draw()
            pygame.display.update()

    def _search(self) -> Union[Node, None]:
        # A*
        frontier: PriorityQueue = PriorityQueue()
        start = Node(location=self._start, parent=None, cost=0, heuristic=self._heuristic(self._start))
        frontier.push(start)
        explored: Dict[Location, int] = {self._start: 0}
        while not frontier.empty:
            current_node: Node = frontier.pop()
            current_location: Location = current_node.location
            # update the screen
            self._maze.mark(location=current_location, color=Cell.EXPLORE)
            self._maze.draw()
            pygame.display.update()
            if self._goal_check(current_location):
                return current_node
            for child in self._successor(current_location, self._allow_diagonal):
                new_cost = current_node.cost + 1
                if child not in explored or explored[child] > new_cost:
                    frontier.push(Node(location=child, parent=current_node,
                                       cost=new_cost, heuristic=self._heuristic(child)))
                    explored[child] = new_cost
        return None

    @property
    def time(self):
        return self._time

    @property
    def len_of_path(self):
        return self._len_of_path
