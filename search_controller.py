from typing import Callable

import pygame

from astar import AStar
from maze import Maze
from utils import Colors, manhattan_distance, euclidean_distance, MazeLocation


class SearchController:
    def __init__(self, maze: Maze, display_surface: pygame.Surface):
        self._maze = maze
        self.display_surface = display_surface
        self._heuristic: Callable[[MazeLocation], Callable[[MazeLocation], float]] = euclidean_distance
        self._font = pygame.font.SysFont("roboto", 24)

        self._euclidean_text = self._font.render("Euclidean Distance", True, Colors.WHITE)
        self._euclidean_rect = self._euclidean_text.get_rect()
        self._euclidean_rect.topleft = (10, 135)

        self._manhattan_text = self._font.render("Manhattan Distance", True, Colors.WHITE)
        self._manhattan_rect = self._manhattan_text.get_rect()
        self._manhattan_rect.topleft = (self._euclidean_rect.right + 10, 135)

    def draw(self):
        # Draw rect for choosing heuristic
        self._draw_heuristic_panel()
        # Draw rect for statistic
        self._draw_statistic_panel()
        pygame.draw.line(self.display_surface, Colors.WHITE, (799, 0), (799, 200), 2)

    def update(self, events: pygame.event):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._run_search()
            if event.type == pygame.MOUSEBUTTONUP:
                if self._manhattan_rect.collidepoint(event.pos):
                    self._heuristic = manhattan_distance
                if self._euclidean_rect.collidepoint(event.pos):
                    self._heuristic = euclidean_distance

    def _draw_heuristic_panel(self):
        pygame.draw.rect(self.display_surface, Colors.BLACK, (0, 0, 800, 200))
        heuristic_name = self._heuristic.__name__.replace("_", " ").title()
        heuristic_text = self._font.render(f"Heuristic Function: {heuristic_name}",
                                           True, Colors.WHITE)
        heuristic_rect = heuristic_text.get_rect()
        heuristic_rect.topleft = (10, 35)
        pygame.draw.line(self.display_surface, Colors.WHITE, (0, 99), (800, 99), 2)
        pygame.draw.line(self.display_surface, Colors.WHITE,
                         (self._manhattan_rect.right + 5, 0),
                         (self._manhattan_rect.right + 5, 200))

        self.display_surface.blit(self._euclidean_text, self._euclidean_rect)
        self.display_surface.blit(self._manhattan_text, self._manhattan_rect)
        self.display_surface.blit(heuristic_text, heuristic_rect)

    def _draw_statistic_panel(self):
        pygame.draw.rect(self.display_surface, Colors.BLACK, (800, 0, 200, 1000))

    def _run_search(self):
        heuristic = self._heuristic(self._maze.goal)
        a_star = AStar(heuristic=heuristic, successor=self._maze.successor,
                       goal_check=self._maze.check_goal, start=self._maze.start, maze=self._maze)
        a_star.start()
