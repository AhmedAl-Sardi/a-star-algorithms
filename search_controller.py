from typing import Callable, Union

import pygame

from astar import AStar
from maze import Maze
from utils import (Colors, manhattan_distance,
                   euclidean_distance, MazeLocation,
                   chebyshev_distance)


class SearchController:
    def __init__(self, maze: Maze, display_surface: pygame.Surface):
        self._maze = maze
        self.display_surface = display_surface
        self._heuristic: Callable[[MazeLocation], Callable[[MazeLocation], float]] = euclidean_distance
        self._font = pygame.font.SysFont("roboto", 24)
        self._a_star: Union[AStar, None] = None

        self._heuristic_panel = pygame.draw.rect(self.display_surface, Colors.BLACK, (0, 0, 800, 200))
        self._statistic_panel = pygame.draw.rect(self.display_surface, Colors.BLACK, (800, 0, 200, 1000))

        self._euclidean_text = self._font.render("Euclidean Distance", True, Colors.WHITE)
        self._euclidean_rect = self._euclidean_text.get_rect()
        self._euclidean_rect.topleft = (10, 135)

        self._manhattan_text = self._font.render("Manhattan Distance", True, Colors.WHITE)
        self._manhattan_rect = self._manhattan_text.get_rect()
        self._manhattan_rect.topleft = (self._euclidean_rect.right + 10, 135)

        self._chebyshev_text = self._font.render("Chebyshev distance", True, Colors.WHITE)
        self._chebyshev_rect = self._chebyshev_text.get_rect()
        self._chebyshev_rect.topleft = (self._manhattan_rect.right + 10, 135)

        self._time_text = self._font.render(f"Time: {0}", True, Colors.WHITE)
        self._time_rect = self._time_text.get_rect()
        self._time_rect.topleft = (self._chebyshev_rect.right + 30, 135)

        self._length_of_path_text = self._font.render(f"Length: {0}", True, Colors.WHITE)
        self._length_of_path_rect = self._length_of_path_text.get_rect()
        self._length_of_path_rect.topleft = (self._chebyshev_rect.right + 30, 35)

    def draw(self):
        # Draw rect for choosing heuristic
        self._draw_heuristic_panel()

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
                if self._chebyshev_rect.collidepoint(event.pos):
                    self._heuristic = chebyshev_distance

    def _draw_heuristic_panel(self):
        self._heuristic_panel = pygame.draw.rect(self.display_surface, Colors.BLACK, (0, 0, 1200, 200))
        heuristic_name = self._heuristic.__name__.replace("_", " ").title()
        heuristic_text = self._font.render(f"Heuristic Function: {heuristic_name}",
                                           True, Colors.WHITE)
        heuristic_rect = heuristic_text.get_rect()
        heuristic_rect.topleft = (10, 35)
        pygame.draw.line(self.display_surface, Colors.WHITE, (0, 99),
                         (self._chebyshev_rect.right + 5, 99), 2)
        pygame.draw.line(self.display_surface, Colors.WHITE,
                         (self._chebyshev_rect.right + 5, 0),
                         (self._chebyshev_rect.right + 5, 200), 2)

        if self._a_star:
            self._time_text = self._font.render(f"Time: {round(self._a_star.time, 3)}", True, Colors.WHITE)
            self._length_of_path_text = self._font.render(f"Length: {self._a_star.len_of_path}", True, Colors.WHITE)
        else:
            self._length_of_path_text = self._font.render(f"Length: {0}", True, Colors.WHITE)
            self._time_text = self._font.render(f"Time: {0}", True, Colors.WHITE)

        self.display_surface.blit(self._euclidean_text, self._euclidean_rect)
        self.display_surface.blit(self._manhattan_text, self._manhattan_rect)
        self.display_surface.blit(self._chebyshev_text, self._chebyshev_rect)
        self.display_surface.blit(heuristic_text, heuristic_rect)
        self.display_surface.blit(self._time_text, self._time_rect)
        self.display_surface.blit(self._length_of_path_text, self._length_of_path_rect)

    def _run_search(self):
        if not self._can_run():
            print("Enter maze value first")
            return
        heuristic = self._heuristic(self._maze.goal)
        self._a_star = AStar(heuristic=heuristic, successor=self._maze.successor,
                             goal_check=self._maze.check_goal, start=self._maze.start, maze=self._maze)
        self._a_star.start()

    def _can_run(self) -> bool:
        if not self._maze.goal or not self._maze.start:
            return False
        return True
