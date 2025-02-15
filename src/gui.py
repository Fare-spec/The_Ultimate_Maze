import pygame
from maze import Maze

def draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color):
    px, py = player_pos
    for y in range(max(0, py - vision_radius), min(maze.height, py + vision_radius + 1)):
        for x in range(max(0, px - vision_radius), min(maze.width, px + vision_radius + 1)):
            cell = maze.grille[y][x]
            x_pixel = (x - px + vision_radius) * cell_size
            y_pixel = (y - py + vision_radius) * cell_size
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
            if cell.get('teleporter', False):
                tp_size = int(cell_size * 0.5)
                offset = (cell_size - tp_size) // 2
                pygame.draw.rect(screen, (0, 255, 0), (x_pixel + offset, y_pixel + offset, tp_size, tp_size))
            
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

def main(difficulty, algorithm, largeur, longueur):
    wall_color = (255, 0, 0) if difficulty == 1 else (0, 0, 0)
    vision_radius = 30
    cell_size = 20

    maze = Maze(largeur, longueur)
    maze.init_labyrinth()
    maze.init_teleporter()
    if algorithm == 1:
        maze.dfs_generation(0, 0)
    else:
        maze.prim_algo(0, 0)

    screen_size = (vision_radius * 2 + 1) * cell_size
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("The Ultimate Maze")
    clock = pygame.time.Clock()

    player_pos = [0, 0]
    tps = maze.get_tp()
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
                if maze.is_tp(player_pos[0],player_pos[1]):
                    if (player_pos[0],player_pos[1]) == tps[0]:
                        player_pos[0], player_pos[1] = tps[1]
                    else:
                        player_pos[0], player_pos[1] = tps[0]
                    
                    maze.remove_tps()


        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color)

        center = vision_radius * cell_size
        pygame.draw.rect(screen, (255, 0, 0), (center + 3, center + 3, cell_size - 6, cell_size - 6))

        pygame.display.flip()
        clock.tick(70)
    pygame.quit()

if __name__ == "__main__":
    difficulty = int(input("Merci d'entrer le niveau de difficulté: \n1)Normal\n2)Impossible\nVotre réponse(1 ou 2): "))
    algorithm = int(input("Merci de choisir l'algorithme de génération du Labyrinthe:\n1)DFS (Depth First Search)\n2)Prim's Algorithm\n(1/2): "))
    largeur = 0
    while largeur < 10:
        largeur = int(input("Merci de choisir la largeur du Labyrinthe (>10): "))
    longueur = 0
    while longueur < 10:
        longueur = int(input("Merci de choisir la longueur du Labyrinthe (>10): "))

    main(difficulty=1, algorithm=1, largeur=10, longueur=10)
