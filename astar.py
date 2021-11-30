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
        self._solution: Node = None
        self._heuristic: Callable[[MazeLocation], float] = heuristic
        self._successor = successor
        self._goal_check = goal_check
        self._start = start
        self._maze: Maze = maze

    @property
    def heuristic(self):
        return self._heuristic

    @heuristic.setter
    def heuristic(self, heuristic):
        self._heuristic = heuristic

    def start(self):
        t1 = time.perf_counter()
        self._solution: Node = self._search(start=self._start, goal_checking=self._goal_check,
                                            heuristic=self._heuristic, successor=self._successor)
        t2 = time.perf_counter()
        print(f"time to take: {t2 - t1}")
        # solution2: Node = self._search(start=start, goal_checking=goal_checking,
        #                                heuristic=heuristic_euclidean, successor=successor)

        if not self._solution:
            print("No solution found")
            return
        paths: List[MazeLocation] = path_to_node(self._solution)
        for location in paths:
            self._maze.mark(location=location, color=Colors.PATH)
            self._maze.draw()
            pygame.display.update()

    def _search(self, start: MazeLocation, goal_checking: Callable[[MazeLocation], bool],
                heuristic: Callable[[MazeLocation], float],
                successor: Callable[[MazeLocation], List[MazeLocation]]) -> Union[Node, None]:
        # A*
        fringe: PriorityQueue = PriorityQueue()
        start = Node(location=start, parent=None, cost=0, heuristic=heuristic(start))
        fringe.push(start)
        explored: Dict[MazeLocation, int] = {start: 0}
        while not fringe.empty:
            current_node: Node = fringe.pop()
            current_location: MazeLocation = current_node.location
            # update the screen
            self._maze.mark(location=current_location, color=Colors.EXPLORE)
            self._maze.draw()
            pygame.display.update()
            if goal_checking(current_location):
                return current_node
            for child in successor(current_location):
                new_cost = current_node.cost
                if child not in explored or explored[child] > new_cost:
                    fringe.push(Node(location=child, parent=current_node,
                                     cost=new_cost, heuristic=heuristic(child)))
                    explored[child] = new_cost
        return None
