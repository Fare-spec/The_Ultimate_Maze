import pygame
from maze import Maze

def draw_maze(maze, screen, cell_size):
    wall_color = (255, 0, 0)
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.grille[y][x]
            x_pixel = x * cell_size
            y_pixel = y * cell_size
            if cell['walls']['N']:
                pygame.draw.line(screen, wall_color,
                                 (x_pixel, y_pixel),
                                 (x_pixel + cell_size, y_pixel), 2)
            if cell['walls']['S']:
                pygame.draw.line(screen, wall_color,
                                 (x_pixel, y_pixel + cell_size),
                                 (x_pixel + cell_size, y_pixel + cell_size), 2)
            if cell['walls']['W']:
                pygame.draw.line(screen, wall_color,
                                 (x_pixel, y_pixel),
                                 (x_pixel, y_pixel + cell_size), 2)
            if cell['walls']['E']:
                pygame.draw.line(screen, wall_color,
                                 (x_pixel + cell_size, y_pixel),
                                 (x_pixel + cell_size, y_pixel + cell_size), 2)

def main():
    maze_width = 20
    maze_height = 20
    cell_size = 60

    maze = Maze(maze_width, maze_height)
    maze.init_labyrinth()
    generation = maze.dfs_generation_step_by_step(0, 0)

    pygame.init()
    screen = pygame.display.set_mode((maze_width * cell_size, maze_height * cell_size))
    pygame.display.set_caption("Génération du Labyrinthe")
    clock = pygame.time.Clock()
    
    generation_done = False
    current_cell = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not generation_done:
            try:
                current_cell = next(generation)
            except StopIteration:
                generation_done = True

        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size)

        if current_cell is not None:
            x, y = current_cell
            highlight_color = (255, 0, 0)
            pygame.draw.rect(screen, highlight_color,
                             (x * cell_size, y * cell_size, cell_size, cell_size), 0)

        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()

