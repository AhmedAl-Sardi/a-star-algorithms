import pygame

from maze import Maze
from maze_controller import MazeController
from utils import Colors

# init

pygame.init()
WIDTH = 1200
HEIGHT = 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Star Algorithms")

FPS = 60
clock = pygame.time.Clock()

maze: Maze = Maze(rows=500, columns=500, grid_size=20,
                  x_offset=0, y_offset=100, display_surface=display_surface)
maze_controller: MazeController = MazeController(maze=maze, display_surface=display_surface)

# main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    maze_controller.update(events=events)

    display_surface.fill(Colors.WHITE)

    maze.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
