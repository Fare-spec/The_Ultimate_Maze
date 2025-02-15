import pygame
from maze import Maze

def draw_maze(maze, screen, cell_size,wall_color):
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

def can_move(maze, x, y, direction):
    cell = maze.grille[y][x]
    if direction == 'UP' and not cell['walls']['N']:
        return True
    if direction == 'DOWN' and not cell['walls']['S']:
        return True
    if direction == 'LEFT' and not cell['walls']['W']:
        return True
    if direction == 'RIGHT' and not cell['walls']['E']:
        return True
    return False

def main(difficulty,algorithm, largeur, longueur):
    if difficulty == 1:
        wall_color = (255,0,0)
    else:
        wall_color = (0,0,0)
    maze_width = largeur
    maze_height = longueur
    cell_size = 20

    maze = Maze(maze_width, maze_height)
    maze.init_labyrinth()
    if algorithm == 1:
        maze.dfs_generation(0,0)
    else:
        maze.prim_algo(0, 0)

    screen = pygame.display.set_mode((maze_width * cell_size + 2, maze_height * cell_size + 2))
    pygame.display.set_caption("The Ultimate Maze")
    clock = pygame.time.Clock()

    player_pos = [0, 0]

    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP and can_move(maze, player_pos[0], player_pos[1], 'UP'):
                    player_pos[1] -= 1
                if event.key == pygame.K_DOWN and can_move(maze, player_pos[0], player_pos[1], 'DOWN'):
                    player_pos[1] += 1
                if event.key == pygame.K_LEFT and can_move(maze, player_pos[0], player_pos[1], 'LEFT'):
                    player_pos[0] -= 1
                if event.key == pygame.K_RIGHT and can_move(maze, player_pos[0], player_pos[1], 'RIGHT'):
                    player_pos[0] += 1

        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size, wall_color)

        pygame.draw.rect(screen, (255, 0, 0), (player_pos[0] * cell_size + 3, player_pos[1] * cell_size + 3, cell_size - 6, cell_size - 6))

        pygame.display.flip()
        clock.tick(70)
    pygame.quit()

if __name__ == "__main__":
    difficulty = int(input("Merci d'entrer le niveau de difficulté: \n1)Normal\n2)Impossible\nVotre réponse(1ou2): "))
    algorithm = int(input("Merci de choisir l'algorithm  de génération du Labyrinth:\n1)DFS(Deepth First Search)\n2)Prim's Algorithm\n(1/2): "))
    largeur = 0
    while largeur < 10:
            largeur = int(input("Merci de choisir la largeur du Labyrinth (>10): "))
    longueur = 0
    while longueur<10:
            longueur = int(input("Merci de choisir la longueur du Labyrinth (>10): "))

    main(difficulty,algorithm, largeur, longueur)
