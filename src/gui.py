import pygame
from maze import Maze
import maze as mz
import pickle

def draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color, chemin=None):
    px, py = player_pos
    base_x, base_y = int(px), int(py)
    offset_x = (px - base_x) * cell_size
    offset_y = (py - base_y) * cell_size

    for y in range(max(0, base_y - vision_radius), min(maze.height, base_y + vision_radius + 1)):
        for x in range(max(0, base_x - vision_radius), min(maze.width, base_x + vision_radius + 1)):
            cell = maze.grille[y][x]
            x_pixel = (x - base_x + vision_radius) * cell_size - offset_x
            y_pixel = (y - base_y + vision_radius) * cell_size - offset_y

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
                offset_rect = (cell_size - tp_size) // 2
                pygame.draw.rect(screen, (0, 255, 0),
                                 (x_pixel + offset_rect, y_pixel + offset_rect, tp_size, tp_size))
    
    if chemin and len(chemin) > 1:
        points = []
        for (cx, cy) in chemin:
            x_pixel = (cx - base_x + vision_radius) * cell_size - offset_x + cell_size // 2
            y_pixel = (cy - base_y + vision_radius) * cell_size - offset_y + cell_size // 2
            points.append((x_pixel, y_pixel))
        pygame.draw.lines(screen, (0, 255, 0), False, points,1)

def animate_movement(maze, start_pos, end_pos, screen, cell_size, vision_radius, wall_color, clock):
    steps = 10
    for step in range(1, steps + 1):
        t = step / steps
        interp_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        interp_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t

        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size, (interp_x, interp_y), vision_radius, wall_color)

        center = vision_radius * cell_size
        pygame.draw.rect(screen, (255, 0, 0), (center + 3, center + 3, cell_size - 6, cell_size - 6))

        pygame.display.flip()
        clock.tick(60)


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
def display_message(screen, text, font_size=36, color=(255, 255, 255), position=(100, 100)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)
def pause_game(screen):
    pygame.display.flip()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    paused = False
def exit_maze(screen, maze, player_pos, cell_size, vision_radius, wall_color, direction):
    for _ in range(5):
        if direction == 'RIGHT':
            player_pos[0] += 0.2
        elif direction == 'DOWN':
            player_pos[1] += 0.2
        
        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color)
        center = vision_radius * cell_size
        pygame.draw.rect(screen, (255, 0, 0), (center + 3, center + 3, cell_size - 6, cell_size - 6))
        pygame.display.flip()
        pygame.time.delay(100)

def main(difficulty, algorithm, largeur, longueur, braid):
    pygame.init()
    pygame.key.set_repeat(200, 50)
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
    if braid == 'o':
        maze.braid_maze(p=0.5)  # Ajuster p pour plus ou moins de randomization
    maze1_len = len(maze.dijkstra(0,0))

    screen_size = (vision_radius * 2 + 1) * cell_size
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("The Ultimate Maze")
    clock = pygame.time.Clock()

    player_pos = [0, 0]
    move_count = 0
    tps = maze.get_tp()
    chemin_dijkstra = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_UP and can_move(maze, player_pos[0], player_pos[1], 'UP'):
                    animate_movement(maze, player_pos, [player_pos[0], player_pos[1] - 1],
                                     screen, cell_size, vision_radius, wall_color, clock)
                    player_pos[1] -= 1
                    move_count += 1
                    chemin_dijkstra = None

                if event.key == pygame.K_DOWN and can_move(maze, player_pos[0], player_pos[1], 'DOWN'):
                    animate_movement(maze, player_pos, [player_pos[0], player_pos[1] + 1],
                                     screen, cell_size, vision_radius, wall_color, clock)
                    player_pos[1] += 1
                    move_count += 1
                    chemin_dijkstra = None

                if event.key == pygame.K_LEFT and can_move(maze, player_pos[0], player_pos[1], 'LEFT'):
                    animate_movement(maze, player_pos, [player_pos[0] - 1, player_pos[1]],
                                     screen, cell_size, vision_radius, wall_color, clock)
                    player_pos[0] -= 1
                    move_count += 1
                    chemin_dijkstra = None

                if event.key == pygame.K_RIGHT and can_move(maze, player_pos[0], player_pos[1], 'RIGHT'):
                    animate_movement(maze, player_pos, [player_pos[0] + 1, player_pos[1]],
                                     screen, cell_size, vision_radius, wall_color, clock)
                    player_pos[0] += 1
                    move_count += 1
                    chemin_dijkstra = None

                if event.key == pygame.K_o:
                    chemin_dijkstra = maze.dijkstra(int(player_pos[0]), int(player_pos[1]))

                if event.key == pygame.K_l:
                    chemin = maze.dijkstra(int(player_pos[0]), int(player_pos[1]))
                    if chemin:
                        for next_pos in chemin[1:]:
                            animate_movement(maze, player_pos, next_pos,
                                             screen, cell_size, vision_radius, wall_color, clock)
                            player_pos = [float(next_pos[0]), float(next_pos[1])]
                            move_count += 1
                        chemin_dijkstra = None

        if maze.is_end(player_pos[0], player_pos[1]):
            optimal_path = maze.dijkstra(0, 0)
            if optimal_path:
                optimal_moves = len(optimal_path) - 1
            else:
                optimal_moves = None

            print("Mouvements réalisés :", move_count)
            print("Nombre de mouvements du chemin optimal :", maze1_len)
            if maze1_len is not None and move_count <= maze1_len:
                print("Vous avez pris le plus court chemin")
            else:
                print("Vous n'avez pas pris le chemin le plus court")

            exit_maze(screen, maze, player_pos, cell_size, vision_radius, wall_color, 'RIGHT')
            display_message(screen, "Bravo ! Vous avez gagné !", 36, (255, 255, 0), (150, 150))
            pygame.display.flip()
            pause_game(screen)

        if maze.is_tp(player_pos[0], player_pos[1]):
            if (player_pos[0], player_pos[1]) == tps[0]:
                player_pos[0], player_pos[1] = tps[1]
            else:
                player_pos[0], player_pos[1] = tps[0]
            maze.remove_tps()
            move_count += 1
            chemin_dijkstra = None

        screen.fill((0, 0, 0))
        draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color, chemin_dijkstra)

        center = vision_radius * cell_size
        pygame.draw.rect(screen, (255, 0, 0), (center + 3, center + 3, cell_size - 6, cell_size - 6))

        pygame.display.flip()
        clock.tick(70)
    pygame.quit()



if __name__ == "__main__":
    default_choice = input(
        "Voulez-vous utiliser les paramètres par défaut ?\n"
        "(DFS, largeur 10, longueur 10, seed aléatoire, braiding activé) (o/n): "
    ).strip().lower()

    if default_choice == "o":

        difficulty = 1
        algorithm = 1
        largeur = 10
        longueur = 10
        seed = ""
        braid = "o"
    else:

        while True:
            try:
                difficulty = int(input(
                    "Merci d'entrer le niveau de difficulté: \n"
                    "1) Normal\n2) Impossible\nVotre réponse (1 ou 2): "
                ))
                if difficulty not in [1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Entrée invalide, veuillez entrer 1 ou 2.")


        seed = input("Veuillez entrer une seed ou laisser vide pour en générer une: ").strip()


        while True:
            try:
                algorithm = int(input(
                    "Merci de choisir l'algorithme de génération du Labyrinthe:\n"
                    "1) DFS (Depth First Search)\n2) Prim's Algorithm\nVotre réponse (1 ou 2): "
                ))
                if algorithm not in [1, 2]:
                    raise ValueError
                break
            except ValueError:
                print("Entrée invalide, veuillez entrer 1 ou 2.")


        while True:
            try:
                largeur = int(input("Merci de choisir la largeur du Labyrinthe (>10): "))
                if largeur < 10:
                    print("La largeur doit être supérieure ou égale à 10.")
                    continue
                break
            except ValueError:
                print("Entrée invalide, veuillez entrer un entier.")


        while True:
            try:
                longueur = int(input("Merci de choisir la longueur du Labyrinthe (>10): "))
                if longueur < 10:
                    print("La longueur doit être supérieure ou égale à 10.")
                    continue
                break
            except ValueError:
                print("Entrée invalide, veuillez entrer un entier.")


        while True:
            braid = input("Voulez-vous que le labyrinthe ait plusieurs chemins (o/n): ").strip().lower()
            if braid in ['o', 'n']:
                break
            else:
                print("Entrée invalide, veuillez répondre par 'o' pour oui ou 'n' pour non.")

    if seed:
        mz.rnd.seed(91842724829)
    else:
        import random
        generated_seed = random.randint(0, 10**12)
        print("Seed générée automatiquement:", generated_seed)
        mz.rnd.seed(generated_seed)

    main(difficulty, algorithm, largeur, longueur, braid)
