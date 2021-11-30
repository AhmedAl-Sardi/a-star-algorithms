import time
from collections import Callable
from typing import Dict, List, Union

import pygame

from maze import Maze
from utils import (PriorityQueue, Node,
                   path_to_node,
                   MazeLocation, Colors)


class AStar:
    def __init__(self, heuristic: Callable[[MazeLocation], float],
                 successor: Callable[[MazeLocation], List[MazeLocation]],
                 goal_check: Callable[[MazeLocation], bool],
                 start: MazeLocation, maze: Maze):
        self._heuristic: Callable[[MazeLocation], float] = heuristic
        self._successor = successor
        self._goal_check = goal_check
        self._start = start
        self._maze: Maze = maze
        self._solution: Union[Node, None] = None
        self._time: float = 0.0
        self._len_of_path: int = 0

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
        paths: List[MazeLocation] = path_to_node(self._solution)
        self._len_of_path = len(paths)
        for location in paths:
            self._maze.mark(location=location, color=Colors.PATH)
            self._maze.draw()
            pygame.display.update()

    def _search(self) -> Union[Node, None]:
        # A*
        fringe: PriorityQueue = PriorityQueue()
        start = Node(location=self._start, parent=None, cost=0, heuristic=self._heuristic(self._start))
        fringe.push(start)
        explored: Dict[MazeLocation, int] = {self._start: 0}
        while not fringe.empty:
            current_node: Node = fringe.pop()
            current_location: MazeLocation = current_node.location
            # update the screen
            self._maze.mark(location=current_location, color=Colors.EXPLORE)
            self._maze.draw()
            pygame.display.update()
            if self._goal_check(current_location):
                return current_node
            for child in self._successor(current_location):
                new_cost = current_node.cost + 1
                if child not in explored or explored[child] > new_cost:
                    fringe.push(Node(location=child, parent=current_node,
                                     cost=new_cost, heuristic=self._heuristic(child)))
                    explored[child] = new_cost
        return None

    @property
    def time(self):
        return self._time

    @property
    def len_of_path(self):
        return self._len_of_path
