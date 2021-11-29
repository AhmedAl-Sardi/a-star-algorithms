import time
from collections import Callable
from typing import Dict, List, Union

import pygame

from maze import Maze
from utils import (PriorityQueue, Node,
                   euclidean_distance, path_to_node,
                   MazeLocation, Colors,
                   manhattan_distance)


class Search:
    def __init__(self, maze: Maze):
        self._maze: Maze = maze

    def start(self):
        # When the user press 'r', grab start location, and heuristic function then start A*
        start: MazeLocation = self._maze.start
        goal_checking: Callable[[MazeLocation], bool] = self._maze.check_goal
        heuristic_manhattan: Callable[[MazeLocation], float] = manhattan_distance(self._maze.goal)
        heuristic_euclidean: Callable[[MazeLocation], float] = euclidean_distance(self._maze.goal)
        successor: Callable[[MazeLocation], List[MazeLocation]] = self._maze.successor

        t1 = time.perf_counter()
        solution: Node = self._search(start=start, goal_checking=goal_checking,
                                      heuristic=heuristic_manhattan, successor=successor)
        t2 = time.perf_counter()
        print(f"time to take: {t2 - t1}")
        # solution2: Node = self._search(start=start, goal_checking=goal_checking,
        #                                heuristic=heuristic_euclidean, successor=successor)

        if not solution:
            print("No solution found")
            return
        paths: List[MazeLocation] = path_to_node(solution)
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
