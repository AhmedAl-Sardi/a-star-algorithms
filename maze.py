import random
from typing import List

import pygame

from utils import Cell, Location


class Maze:
    def __init__(self, rows: int, columns: int,
                 grid_size: int, x_offset: int, y_offset: int,
                 display_surface: pygame.Surface,
                 start: Location = None, goal: Location = None):
        self.x = columns
        self.y = rows
        self._grid_size: int = grid_size
        self._rows: int = self.x // self._grid_size
        self._columns: int = self.y // self._grid_size
        self._x_offset: int = x_offset
        self._y_offset: int = y_offset
        self._start: Location = start
        self._goal: Location = goal
        self.display_surface = display_surface

        self._grid = [[Cell.WHITE for _ in range(self._columns)]
                      for _ in range(self._rows)]

    def check_goal(self, location: Location) -> bool:
        return self._goal == location

    def successor(self, location: Location, allow_diagonal=False) -> List[Location]:
        list_of_neighbor: List[Location] = []
        # the order: Top, Right, Bottom, Left
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

    def mark(self, location: Location, color: Cell) -> None:
        value = self._grid[location.row][location.column]
        if value != Cell.START and value != Cell.GOAL:
            self._grid[location.row][location.column] = color

    def draw(self):
        # vertical line
        self._draw_vertical_line()
        # horizontal line
        self._draw_horizontal_line()

        self._draw_occupied_place()

    @property
    def start(self) -> Location:
        return self._start

    @start.setter
    def start(self, location: Location):
        start: Location = self._normalize_location(location=location)
        # Todo: Check for boundary before assign
        if not self._check_boundary(location=start):
            return None
        self._start = start
        # Todo: check if there are start point in grid before adding the new one
        self._change_location_state(from_state=Cell.START, to=Cell.WHITE)
        self._grid[self._start.row][self._start.column] = Cell.START

    @property
    def goal(self) -> Location:
        return self._goal

    @goal.setter
    def goal(self, location: Location):
        goal: Location = self._normalize_location(location=location)
        # Todo: check for boundary before assign
        if not self._check_boundary(location=goal):
            return None
        self._goal = goal
        self._change_location_state(from_state=Cell.GOAL, to=Cell.WHITE)
        self._grid[self._goal.row][self._goal.column] = Cell.GOAL

    def block(self, location: Location, to: Cell = Cell.BLOCK):
        block: Location = self._normalize_location(location=location)
        # Todo: check for boundary before assign
        if not self._check_boundary(location=block):
            return None
        if self._grid[block.row][block.column] == Cell.WHITE or self._grid[block.row][block.column] == Cell.BLOCK:
            self._grid[block.row][block.column] = to

    def erase_maze(self):
        self._grid = [[Cell.WHITE for _ in range(self._columns)]
                      for _ in range(self._rows)]

    def clear_maze(self):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == Cell.EXPLORE or value == Cell.PATH:
                    self._grid[i][j] = Cell.WHITE

    def fill_random(self, spread: float = 0.2):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == Cell.WHITE and random.uniform(0, 1) < spread:
                    self._grid[i][j] = Cell.BLOCK
                    self.draw()
                    pygame.display.update()

    def _draw_horizontal_line(self):
        # Draw Horizontal Line
        for i in range(self._columns + 1):
            pygame.draw.line(self.display_surface, Cell.GARY,
                             (self._x_offset, i * self._grid_size + self._y_offset),
                             (self._x_offset + self.x, (i * self._grid_size) + self._y_offset))

    def _draw_vertical_line(self):
        # Draw Vertical Line
        for i in range(self._rows + 1):
            pygame.draw.line(self.display_surface, Cell.GARY,
                             (i * self._grid_size + self._x_offset, self._y_offset),
                             (i * self._grid_size + self._x_offset, self._y_offset + self.y))

    def _change_location_state(self, from_state: Cell, to: Cell):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value == from_state:
                    self._grid[i][j] = to

    def _normalize_location(self, location: Location) -> Location:
        x = (location.row - self._x_offset) // self._grid_size
        y = (location.column - self._y_offset) // self._grid_size
        return Location(x, y)

    def _draw_occupied_place(self):
        for i, row in enumerate(self._grid):
            for j, value in enumerate(row):
                if value is not Cell.WHITE:
                    self._draw_rect(x=i, y=j, value=value)

    def _draw_rect(self, x: int, y: int, value: Cell):
        rect_x = (x * self._grid_size) + self._x_offset
        rect_y = (y * self._grid_size) + self._y_offset
        pygame.draw.rect(self.display_surface, value,
                         (rect_x + 1, rect_y + 1, self._grid_size - 1, self._grid_size - 1))

    def _check_boundary(self, location: Location):
        if 0 <= location.row < self._rows and 0 <= location.column < self._columns:
            return True
        return False
