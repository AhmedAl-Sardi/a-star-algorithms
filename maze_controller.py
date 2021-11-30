from enum import Enum

import pygame

from maze import Maze
from utils import MazeLocation


class MazeControllerCommand(str, Enum):
    BLOCK = "BLOCK"
    START = "START"
    GOAL = "GOAL"
    ERASE = "ERASE"
    ERASE_EXPLORE_AND_PATH = "ERASE EXPLORE AND PATH"


class MazeController:
    def __init__(self, maze: Maze, display_surface: pygame.Surface):
        self._maze = maze
        self.display_grid = display_surface
        self._current_command: MazeControllerCommand = MazeControllerCommand.START

    def update(self, events: pygame.event):
        # Loop for event and allow user to:
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._change_current_command(event)
            if self._current_command == MazeControllerCommand.START:
                self._check_for_start_point(event=event)
            if self._current_command == MazeControllerCommand.GOAL:
                self._check_for_goal_point(event=event)
            if self._current_command == MazeControllerCommand.BLOCK:
                self._check_for_block_point(event=event)
            if self._current_command == MazeControllerCommand.ERASE:
                self._erase_maze()
                self._current_command = MazeControllerCommand.START
            if self._current_command == MazeControllerCommand.ERASE_EXPLORE_AND_PATH:
                self._erase_explore_and_path()

    def _change_current_command(self, event):
        if event.key == pygame.K_s:
            self._current_command = MazeControllerCommand.START
        if event.key == pygame.K_g:
            self._current_command = MazeControllerCommand.GOAL
        if event.key == pygame.K_b:
            self._current_command = MazeControllerCommand.BLOCK
        if event.key == pygame.K_e:
            self._current_command = MazeControllerCommand.ERASE
        if event.key == pygame.K_p:
            self._current_command = MazeControllerCommand.ERASE_EXPLORE_AND_PATH

    def _check_for_start_point(self, event: pygame.event):
        # press 's' and mouse click, then add start point to maze
        if event.type == pygame.MOUSEBUTTONUP:
            self._maze.start = (MazeLocation(row=event.pos[0], column=event.pos[1]))

    def _check_for_goal_point(self, event: pygame.event):
        # press 'g' and mouse click, then add goal point to maze
        if event.type == pygame.MOUSEBUTTONUP:
            self._maze.goal = (MazeLocation(row=event.pos[0], column=event.pos[1]))

    def _check_for_block_point(self, event: pygame.event):
        if event.type == pygame.MOUSEMOTION and event.buttons[0]:
            self._maze.block(location=MazeLocation(event.pos[0], column=event.pos[1]))

    def _erase_maze(self):
        self._maze.erase_maze()

    def _erase_explore_and_path(self):
        self._maze.erase_explore_and_path()
        self._current_command = MazeControllerCommand.BLOCK
