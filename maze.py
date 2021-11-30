from typing import List

import pygame

from utils import Colors, MazeLocation


class Maze:
    def __init__(self, rows: int, columns: int,
                 grid_size: int, x_offset: int, y_offset: int,
                 display_surface: pygame.Surface,
                 start: MazeLocation = None, goal: MazeLocation = None):
        self.x = columns
        self.y = rows
        self._grid_size: int = grid_size
        self._rows: int = self.x // self._grid_size
        self._columns: int = self.y // self._grid_size
        self._x_offset: int = x_offset
        self._y_offset: int = y_offset
        self._start: MazeLocation = start
        self._goal: MazeLocation = goal
        self.display_surface = display_surface

        self._grid = [[Colors.WHITE for _ in range(self._columns)]
                      for _ in range(self._rows)]

    def check_goal(self, location: MazeLocation) -> bool:
        return self._goal == location

    def successor(self, location: MazeLocation) -> List[MazeLocation]:
        list_of_neighbor: List[MazeLocation] = []
        # the order: Top, Right, Bottom, Left
        if location.column - 1 >= 0 and self._grid[location.row][location.column - 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row, location.column - 1))
        if location.row + 1 < self._rows and self._grid[location.row + 1][location.column] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row + 1, location.column))
        if location.column + 1 < self._columns and self._grid[location.row][location.column + 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row, location.column + 1))
        if location.row - 1 >= 0 and self._grid[location.row - 1][location.column] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row - 1, location.column))
        # Check for diagonal neighbor
        # top-right
        if (location.column - 1 >= 0 and location.row + 1 < self._rows) and self._grid[
            location.row + 1][location.column - 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row + 1, location.column - 1))
        # bottom-right
        if (location.column + 1 < self._columns and location.row + 1 < self._rows) and self._grid[
            location.row + 1][location.column + 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row + 1, location.column + 1))
        # bottom - left
        if (location.column + 1 < self._columns and location.row - 1 >= 0) and self._grid[
            location.row - 1][location.column + 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row - 1, location.column + 1))
        # top-left
        if (location.column - 1 >= 0 and location.row - 1 >= 0) and self._grid[
            location.row - 1][location.column - 1] != Colors.BLACK:
            list_of_neighbor.append(MazeLocation(location.row - 1, location.column - 1))
        return list_of_neighbor

    def mark(self, location: MazeLocation, color: Colors) -> None:
        value = self._grid[location.row][location.column]
        if value != Colors.START and value != Colors.GOAL:
            self._grid[location.row][location.column] = color

    def draw(self):
        # vertical line
        self._draw_vertical_line()
        # horizontal line
        self._draw_horizontal_line()

        self._draw_occupied_place()

    def _draw_horizontal_line(self):
        # Draw Horizontal Line
        for i in range(self._columns + 1):
            pygame.draw.line(self.display_surface, Colors.GARY,
                             (self._x_offset, i * self._grid_size + self._y_offset),
                             (self._x_offset + self.x, (i * self._grid_size) + self._y_offset))

    def _draw_vertical_line(self):
        # Draw Vertical Line
        for i in range(self._rows + 1):
            pygame.draw.line(self.display_surface, Colors.GARY,
                             (i * self._grid_size + self._x_offset, self._y_offset),
                             (i * self._grid_size + self._x_offset, self._y_offset + self.y))

    @property
    def start(self) -> MazeLocation:
        return self._start

    @start.setter
    def start(self, location: MazeLocation):
        start: MazeLocation = self._normalize_location(location=location)
        # Todo: Check for boundary before assign
        if not self._check_boundary(location=start):
            return None
        self._start = start
        # Todo: check if there are start point in grid before adding the new one
        self._change_location_state(from_state=Colors.START, to=Colors.WHITE)
        self._grid[self._start.row][self._start.column] = Colors.START

    @property
    def goal(self) -> MazeLocation:
        return self._goal

    @goal.setter
    def goal(self, location: MazeLocation):
        goal: MazeLocation = self._normalize_location(location=location)
        # Todo: check for boundary before assign
        if not self._check_boundary(location=goal):
            return None
        self._goal = goal
        self._change_location_state(from_state=Colors.GOAL, to=Colors.WHITE)
        self._grid[self._goal.row][self._goal.column] = Colors.GOAL

    def block(self, location: MazeLocation):
        block: MazeLocation = self._normalize_location(location=location)
        # Todo: check for boundary before assign
        if not self._check_boundary(location=block):
            return None
        if self._grid[block.row][block.column] == Colors.WHITE:
            self._grid[block.row][block.column] = Colors.BLACK

    def _change_location_state(self, from_state: Colors, to: Colors):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == from_state:
                    self._grid[i][j] = to

    def _normalize_location(self, location: MazeLocation) -> MazeLocation:
        x = (location.row - self._x_offset) // self._grid_size
        y = (location.column - self._y_offset) // self._grid_size
        return MazeLocation(x, y)

    def _draw_occupied_place(self):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value is not Colors.WHITE:
                    self._draw_rect(x=i, y=j, value=value)

    def _draw_rect(self, x: int, y: int, value: Colors):
        rect_x = (x * self._grid_size) + self._x_offset
        rect_y = (y * self._grid_size) + self._y_offset
        pygame.draw.rect(self.display_surface, value,
                         (rect_x + 1, rect_y + 1, self._grid_size - 1, self._grid_size - 1))

    def _check_boundary(self, location: MazeLocation):
        if 0 <= location.row < self._rows and 0 <= location.column < self._columns:
            return True
        return False

    def erase_maze(self):
        self._grid = [[Colors.WHITE for _ in range(self._columns)]
                      for _ in range(self._rows)]

    def erase_explore_and_path(self):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == Colors.EXPLORE or value == Colors.PATH:
                    self._grid[i][j] = Colors.WHITE
