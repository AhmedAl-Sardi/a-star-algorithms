from typing import Callable, List, Dict

from a_star_terminal.utils import (PriorityQueue, Node,
                                   Location)


def a_star(start: Location, goal_check: Callable[[Location], bool],
           successor: Callable[[Location, bool], List[Location]], heuristic: Callable[[Location], float],
           allow_diagonal: bool):
    """
    Implementation of A* algorithms
    :param start: start location
    :param goal_check: reference of method to test if the location is the goal
    :param successor: reference of method to get all the available location from giving location
    :param heuristic: reference of method to get the heuristic cost of giving location to goal location
    :param allow_diagonal: allow for diagonal movement
    :return:
    """
    frontier = PriorityQueue()
    node = Node(start, None, 0, heuristic(start))
    frontier.push(node)
    explored: Dict[Location, int] = {start: 0}
    while not frontier.empty:
        current_node = frontier.pop()
        if goal_check(current_node.location):
            return current_node
        for child in successor(current_node.location, allow_diagonal=allow_diagonal):
            new_cost = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
                explored[child] = new_cost
    return None
