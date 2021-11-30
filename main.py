import pygame

from maze import Maze
from maze_controller import MazeController
from search_controller import SearchController
from utils import Colors

# init

pygame.init()
WIDTH = 1200
HEIGHT = 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Star Algorithms")

FPS = 60
clock = pygame.time.Clock()

maze: Maze = Maze(rows=600, columns=1200, grid_size=20,
                  x_offset=0, y_offset=200, display_surface=display_surface)
maze_controller: MazeController = MazeController(maze=maze, display_surface=display_surface)
search_controller: SearchController = SearchController(maze=maze, display_surface=display_surface)

# main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    search_controller.update(events=events)
    maze_controller.update(events=events)

    display_surface.fill(Colors.WHITE)
    search_controller.draw()
    maze.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
