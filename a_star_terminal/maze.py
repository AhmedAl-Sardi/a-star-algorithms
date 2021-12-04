import random
from typing import List

from a_star_terminal.a_star import a_star
from a_star_terminal.utils import (Location, Cell, euclidean_distance,
                                   manhattan_distance, Node, path_to_node, chebyshev_distance)


class Maze:
    def __init__(self, rows: int, columns: int, start_location: Location, goal_location: Location):
        self._rows = rows
        self._columns = columns
        self._start: Location = start_location
        self._goal: Location = goal_location
        self._grid = [[Cell.EMPTY for _ in range(columns)]
                      for _ in range(rows)]
        self._grid[start_location.row][start_location.column] = Cell.START
        self._grid[goal_location.row][goal_location.column] = Cell.GOAL
        self._fill_random()

    def successor(self, location: Location, allow_diagonal=False) -> List[Location]:
        """
        Given a location, return all the possible state of the location
        :param allow_diagonal
        :param location
        :return: list of available location
        """
        list_of_neighbor: List[Location] = []
        if location.column - 1 >= 0 and self._grid[location.row][location.column - 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row, location.column - 1))
        if location.row + 1 < self._rows and self._grid[location.row + 1][location.column] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row + 1, location.column))
        if location.column + 1 < self._columns and self._grid[location.row][location.column + 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row, location.column + 1))
        if location.row - 1 >= 0 and self._grid[location.row - 1][location.column] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row - 1, location.column))
            # Check for diagonal neighbor if possible
        if not allow_diagonal:
            return list_of_neighbor
        # top-right
        if (location.column - 1 >= 0 and location.row + 1 < self._rows) and self._grid[
            location.row + 1][location.column - 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row + 1, location.column - 1))
        # bottom-right
        if (location.column + 1 < self._columns and location.row + 1 < self._rows) and self._grid[
            location.row + 1][location.column + 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row + 1, location.column + 1))
        # bottom - left
        if (location.column + 1 < self._columns and location.row - 1 >= 0) and self._grid[
            location.row - 1][location.column + 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row - 1, location.column + 1))
        # top-left
        if (location.column - 1 >= 0 and location.row - 1 >= 0) and self._grid[
            location.row - 1][location.column - 1] != Cell.BLOCK:
            list_of_neighbor.append(Location(location.row - 1, location.column - 1))
        return list_of_neighbor

    def goal_check(self, location: Location) -> bool:
        """
        Check if the location is the same as goal
        :param location
        :return: bool
        """
        return self._goal == location

    def mark(self, paths: List[Location]):
        """
        Mark all the location in path as PATH
        :param paths: List of location
        """
        for location in paths:
            self._grid[location.row][location.column] = Cell.PATH
        self._grid[self._start.row][self._start.column] = Cell.START
        self._grid[self._goal.row][self._goal.column] = Cell.GOAL

    def __str__(self):
        """
        represent maze in the terminal
        :return: maze representation: str
        """
        output = ""
        for row in self._grid:
            output += "".join([cell.value for cell in row]) + "\n"
        return output

    def _fill_random(self):
        """
        Create random block, each cell have 0.2 chance to be BLOCK
        """
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == Cell.EMPTY and random.uniform(0, 1) < 0.2:
                    self._grid[i][j] = Cell.BLOCK


if __name__ == '__main__':
    start = Location(0, 0)
    goal = Location(9, 9)
    euclidean_heuristic = euclidean_distance(goal)
    manhattan_heuristic = manhattan_distance(goal)
    chebyshev_heuristic = chebyshev_distance(goal)
    maze: Maze = Maze(10, 10, start, goal)
    solution: Node = a_star(start, maze.goal_check, maze.successor, chebyshev_heuristic, True)
    print(maze)
    if not solution:
        print("No solution is found")
    else:
        path = path_to_node(solution)
        maze.mark(path)
        print(maze)
