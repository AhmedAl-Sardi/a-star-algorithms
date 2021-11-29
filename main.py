import pygame

# init
from maze import Maze
from utils import Colors

pygame.init()
WIDTH = 1200
HEIGHT = 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Star Algorithms")

FPS = 60
clock = pygame.time.Clock()

maze: Maze = Maze(rows=500, columns=500, grid_size=20,
                  x_offset=0, y_offset=100, display_surface=display_surface)

# main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_surface.fill(Colors.WHITE)

    maze.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
