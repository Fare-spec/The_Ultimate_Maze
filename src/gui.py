import pygame
from maze import Maze

def draw_maze(maze, screen, cell_size):
    wall_color = (0, 0, 0)
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
    maze_width = 600
    maze_height = 600
    cell_size = 10

    maze = Maze(maze_width, maze_height)
    maze.init_labyrinth()
    maze.kruskal_generation()

    screen = pygame.display.set_mode((maze_width * cell_size + 2, maze_height * cell_size + 2))
    pygame.display.set_caption("The Ultimate Maze")
    clock = pygame.time.Clock()
    
    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill((255, 255, 255))
        draw_maze(maze, screen, cell_size)
        pygame.display.flip()
        clock.tick(70)
    pygame.quit()

if __name__ == "__main__":
    main()
