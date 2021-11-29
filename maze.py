from typing import NamedTuple

import pygame

from utils import Colors


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(self, rows: int, columns: int,
                 grid_size: int, x_offset: int, y_offset: int,
                 display_surface: pygame.Surface,
                 start: MazeLocation = None, goal: MazeLocation = None):
        self._rows: int = rows
        self._columns: int = columns
        self._grid_size: int = grid_size
        self._x_offset: int = x_offset
        self._y_offset: int = y_offset
        self._start: MazeLocation = start
        self._goal: MazeLocation = goal
        self.display_surface = display_surface

        self._grid = [[Colors.WHITE for _ in range(self._columns)] for _ in range(self._rows)]

    def check_goal(self):
        pass

    def successor(self):
        pass

    def mark(self):
        pass

    def update(self):
        pass

    def draw(self):
        # vertical line
        self._draw_vertical_line()
        # horizontal line
        self._draw_horizontal_line()

        # Todo: Get the list of occupied places

        # Todo: Draw all rect in these occupied places

    def _draw_horizontal_line(self):
        # Draw Horizontal Line
        for i in range((self._columns // self._grid_size) + 1):
            pygame.draw.line(self.display_surface, Colors.GARY,
                             (self._x_offset, i * self._grid_size + self._y_offset),
                             (self._x_offset + self._columns, (i * self._grid_size) + self._y_offset))

    def _draw_vertical_line(self):
        # Draw Vertical Line
        for i in range((self._rows // self._grid_size) + 1):
            pygame.draw.line(self.display_surface, Colors.GARY,
                             (i * self._grid_size + self._x_offset, self._y_offset),
                             (i * self._grid_size + self._x_offset, self._y_offset + self._rows))

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, location: MazeLocation):
        self._start = location

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, location: MazeLocation):
        self._goal = location
