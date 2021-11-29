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

        self._grid = [[Colors.WHITE for _ in range(self._columns // self._grid_size)]
                      for _ in range(self._rows // self._grid_size)]

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
        self._draw_occupied_place()

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
    def start(self) -> MazeLocation:
        return self._start

    def set_start(self, location: MazeLocation):
        start: MazeLocation = self._normalize_location(location=location)
        self._start = start
        print("update the start location")
        # Todo: check if there are start point in grid before adding the new one
        self._change_location_state(from_state=Colors.START, to=Colors.WHITE)
        self._grid[self._start.row][self._start.column] = Colors.START

    @property
    def goal(self) -> MazeLocation:
        return self._goal

    def set_goal(self, location: MazeLocation):
        goal: MazeLocation = self._normalize_location(location=location)
        self._goal = goal
        print("update the goal location")
        # Todo: check if there are goal in grid before adding the goal
        self._change_location_state(from_state=Colors.GOAL, to=Colors.WHITE)
        self._grid[self._goal.row][self._goal.column] = Colors.GOAL

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
                         (rect_x, rect_y, self._grid_size, self._grid_size))
