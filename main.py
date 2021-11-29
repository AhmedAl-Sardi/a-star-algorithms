import pygame

from maze import Maze
from maze_controller import MazeController
from search import Search
from utils import Colors

# init

pygame.init()
WIDTH = 1200
HEIGHT = 800
display_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Star Algorithms")

FPS = 60
clock = pygame.time.Clock()

maze: Maze = Maze(rows=700, columns=800, grid_size=20,
                  x_offset=0, y_offset=100, display_surface=display_surface)
maze_controller: MazeController = MazeController(maze=maze, display_surface=display_surface)
search: Search = Search(maze=maze)

# main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                search.start()
    maze_controller.update(events=events)

    display_surface.fill(Colors.WHITE)

    maze.draw()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
