import sys
import pygame
import random
from maze import Maze
import maze as mz

COLOR_WALL = (255, 0, 0)
COLOR_TELEPORTER = (0, 255, 0)
COLOR_HELP_PATH = (0, 255, 0)
COLOR_TRAVELED_PATH = (0, 0, 255)
COLOR_PLAYER = (255, 0, 0)
COLOR_BG = (0, 0, 0)
COLOR_MESSAGE = (255, 255, 0)
COLOR_PACMAN = (255, 255, 0)

def draw_labyrinth(maze, screen, cell_size, state=None):
    """Dessine le labyrinthe de façon statique (montre la génération)

    Args:
        maze (Maze): L'objet maze avec ces attribut a dessiner.
        screen (Pygame):Une classe de pygame utilisé pour afficher le labyrinthe a l'ecran grace au propriéter ci dessus 
        cell_size (int): la taille de la cellule affiche a l'ecran
        state (dict, optional):  contient des infos sur la generation ou l'animation du labirynthe. Defaults to None.
    """
    screen.fill((0, 0, 0))
    wall_color = (255, 0, 0)
    for y in range(maze.height):
        for x in range(maze.width):
            x_pix = x * cell_size
            y_pix = y * cell_size
            cell = maze.grille[y][x]
            if cell['walls']['N']:
                pygame.draw.line(screen, wall_color, (x_pix, y_pix), (x_pix + cell_size, y_pix), 2)
            if cell['walls']['S']:
                pygame.draw.line(screen, wall_color, (x_pix, y_pix + cell_size), (x_pix + cell_size, y_pix + cell_size), 2)
            if cell['walls']['W']:
                pygame.draw.line(screen, wall_color, (x_pix, y_pix), (x_pix, y_pix + cell_size), 2)
            if cell['walls']['E']:
                pygame.draw.line(screen, wall_color, (x_pix + cell_size, y_pix), (x_pix + cell_size, y_pix + cell_size), 2)
    if state is not None and "current" in state:
        cx, cy = state["current"]
        pygame.draw.rect(screen, (255, 0, 0), (cx * cell_size, cy * cell_size, cell_size, cell_size), 3)
    pygame.display.flip()

def draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color, help_path=None, traveled_path=None):
    """affiche le labyrinthe en mode POV du joueur

    Args:
        maze (Maze): L'objet maze contenant toutes les infos du labyrinthe
        screen (Pygame): La fenêtre pygame
        cell_size (int): la taille de la cellule
        player_pos (tuple): la position actuelle du joueur (permet d'afficher le labyrinthe autour du joueur)
        vision_radius (int): la distances autour du joueur qui doit etre visible
        wall_color (tuple): la couleur des murs
        help_path (list, optional): La liste des coordonnées représentant le chemin. Defaults to None.
        traveled_path (list, optional): Le chemin déjà parcourus. Defaults to None.
    """
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
                pygame.draw.line(screen, wall_color, (x_pixel, y_pixel), (x_pixel + cell_size, y_pixel), 2)
            if cell['walls']['S']:
                pygame.draw.line(screen, wall_color, (x_pixel, y_pixel + cell_size), (x_pixel + cell_size, y_pixel + cell_size), 2)
            if cell['walls']['W']:
                pygame.draw.line(screen, wall_color, (x_pixel, y_pixel), (x_pixel, y_pixel + cell_size), 2)
            if cell['walls']['E']:
                pygame.draw.line(screen, wall_color, (x_pixel + cell_size, y_pixel), (x_pixel + cell_size, y_pixel + cell_size), 2)
            if cell.get('teleporter', False):
                tp_size = int(cell_size * 0.5)
                offset_rect = (cell_size - tp_size) // 2
                pygame.draw.rect(screen, COLOR_TELEPORTER, (x_pixel + offset_rect, y_pixel + offset_rect, tp_size, tp_size))
    if help_path and len(help_path) > 1:
        points = []
        for (cx, cy) in help_path:
            x_pixel = (cx - base_x + vision_radius) * cell_size - offset_x + cell_size // 2
            y_pixel = (cy - base_y + vision_radius) * cell_size - offset_y + cell_size // 2
            points.append((x_pixel, y_pixel))
        pygame.draw.lines(screen, COLOR_HELP_PATH, False, points, 1)
    if traveled_path and len(traveled_path) > 1:
        points = []
        for (cx, cy) in traveled_path:
            x_pixel = (cx - base_x + vision_radius) * cell_size - offset_x + cell_size // 2
            y_pixel = (cy - base_y + vision_radius) * cell_size - offset_y + cell_size // 2
            points.append((x_pixel, y_pixel))
        pygame.draw.lines(screen, COLOR_TRAVELED_PATH, False, points, 2)

def animate_movement(maze: Maze, start_pos:tuple, end_pos: tuple, screen: pygame, cell_size: int, vision_radius:int, wall_color:tuple, clock:pygame):
    """Sert a animer e mouvement du labyrinthe pour eviter qu'il soit trop saccadé

    Args:
        maze (Maze):  L'objet maze contenant toutes les infos du labyrinthe
        start_pos (tuple): les coordonnées du debut
        end_pos (tuple): les coo de la fin
        screen (pygame): la fenetre
        cell_size (int): la taille de chaque cellules
        vision_radius (int): le champ de vision du joueur
        wall_color (tuple): la couleurs des murs
        clock (pygame): l'horloge de pygame (notament pour les fps)
    """
    steps = 10 # peut etre ajuster pour que ce soit plus doux ou pas 
    
    for step in range(1, steps + 1):
        t = step / steps
        interp_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        interp_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        screen.fill(COLOR_BG)
        draw_maze(maze, screen, cell_size, (interp_x, interp_y), vision_radius, wall_color)
        center = vision_radius * cell_size
        pygame.draw.rect(screen, COLOR_PLAYER, (center + 3, center + 3, cell_size - 6, cell_size - 6))
        pygame.display.flip()
        clock.tick(60)

def can_move(maze: Maze, x: int, y: int, direction: str)->bool:
    """fonction qui permet de savoir si le joueur peut bouger ou s'il est en collision avec un mur

    Args:
        maze (Maze): le labyrinthe
        x (int): coo du joueur en absisses
        y (int): coo du joueur en ordonnée
        direction (str): la direction dans laquelle il veut aller

    Returns:
        bool: can move ou pas
    """

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

def display_message(screen:pygame, text:str, font_size:int=36, color:tuple=(255,255,255), position:tuple=(100,100)):
    """fonction qui affiche un message dans la fenetre

    Args:
        screen (pygame): la fenetre
        text (str): le message
        font_size (int, optional): la taille du texte. Defaults to 36.
        color (tuple, optional): la couleur. Defaults to (255,255,255).
        position (tuple, optional): la position. Defaults to (100,100).
    """
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def pause_game(screen):
    """mets en pause la vue sur le labyrinthe

    Args:
        screen (pygame): la fenetre
    """
    pygame.display.flip()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE]:
                    paused = False

def exit_maze(screen:pygame, maze:Maze, player_pos:tuple, cell_size:int, vision_radius:int, wall_color:tuple, direction:str):
    """fait une animation pour sortir du labyrinthe et empeche une erreur list index out of range...
    les arguments restent inchangé

    Args:
        screen (pygame): _description_
        maze (Maze): _description_
        player_pos (tuple): _description_
        cell_size (int): _description_
        vision_radius (int): _description_
        wall_color (tuple): _description_
        direction (str): _description_
    """
    for _ in range(5):
        if direction == 'RIGHT':
            player_pos[0] += 0.2
        elif direction == 'DOWN':
            player_pos[1] += 0.2
        screen.fill(COLOR_BG)
        draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color)
        center = vision_radius * cell_size
        pygame.draw.rect(screen, COLOR_PLAYER, (center + 3, center + 3, cell_size - 6, cell_size - 6))
        pygame.display.flip()
        pygame.time.delay(100)

def get_game_parameters():
    """demande a l'utilisateur les paramêtre dans lesquel il veut lancer son labyrinthe
    """
    default_choice = input(
        "Voulez-vous utiliser les paramètres par défaut ?\n"
        "(DFS, largeur 20, longueur 20, seed aléatoire, braiding activé,difficulté: normale, animation) (o/n): "
    ).strip().lower()
    if default_choice == "o":
        return {"difficulty": 1, "algorithm": 1, "largeur": 10, "longueur": 10, "seed": "", "braid": "o","show_gen":"o","pacman":"o"}
    else:
        while True:
            try:
                difficulty = int(input(
                    "Merci d'entrer le niveau de difficulté: \n"
                    "1) Normal\n2) Impossible\n3) Difficile\nVotre réponse (1, 2, 3): "
                ))
                if difficulty not in [1, 2, 3]:
                    raise Exception
                break
            except Exception:
                print("Entrée invalide, veuillez entrer 1, 2 ou 3.")
        seed = input("Veuillez entrer une seed ou laisser vide pour en générer une: ").strip()
        while True:
            try:
                algorithm = int(input(
                    "Merci de choisir l'algorithme de génération du Labyrinthe:\n"
                    "1) DFS (Depth First Search)\n2) Prim's Algorithm\nVotre réponse (1 ou 2): "
                ))
                if algorithm not in [1, 2]:
                    raise Exception
                break
            except Exception:
                print("Entrée invalide, veuillez entrer 1 ou 2.")
        while True:
            try:
                largeur = int(input("Merci de choisir la largeur du Labyrinthe (>=10): "))
                if largeur < 10:
                    print("La largeur doit être supérieure ou égale à 10.")
                    continue
                break
            except Exception:
                print("Entrée invalide, veuillez entrer un entier.")
        while True:
            try:
                longueur = int(input("Merci de choisir la longueur du Labyrinthe (>=10): "))
                if longueur < 10:
                    print("La longueur doit être supérieure ou égale à 10.")
                    continue
                break
            except Exception:
                print("Entrée invalide, veuillez entrer un entier.")
        while True:
            try:
                show_gen = input("Voulez-vous voir l'animation de génération du labyrinthe ? (o/n): ").strip().lower()
                if show_gen not in["o","n"]:
                    continue
                else:
                    break
            except Exception:
                print("Entrée invalide, veuillez répondre par 'o' ou 'n'.")
        while True:
            try:
                pacman = input("Voulez-vous avoir un ennemi ?(o/n): ").strip().lower()
                if pacman in ["o","n"]:
                    break
                else:
                    print("Entrée invalide, veuillez répondre par 'o' ou 'n'.")
            except Exception:
                print("Entrée invalide, veuillez répondre par 'o' ou 'n'.")

        while True:
            braid = input("Voulez-vous que le labyrinthe ait plusieurs chemins (o/n): ").strip().lower()
            if braid in ['o', 'n']:
                break
            else:
                print("Entrée invalide, veuillez répondre par 'o' ou 'n'.")
        return {"difficulty": difficulty, "algorithm": algorithm, "largeur": largeur, "longueur": longueur, "seed": seed, "braid": braid, "show_gen": show_gen,"pacman":pacman}

def main(difficulty: int, algorithm: int, largeur: int, longueur: int, braid:str, show_gen:str, pacman_choice:str):
    """initialise tout

    Args:
        difficulty (int): la difficulté (1,2,3)
        algorithm (int): l'algo a utiliser (1,2)
        largeur (int): la largeur
        longueur (int): la longueur
        braid (str): si on veut que le labyrithe ait des murs random supprimé
        show_gen (str): si on veut afficher la generation du labyrinthe
        pacman_choice (str): si on veut un gentil ennemi
    """
    pygame.init()
    pygame.key.set_repeat(200, 50)
    wall_color = COLOR_WALL if difficulty in [1, 3] else (0, 0, 0)
    vision_radius = 30
    cell_size = 20

    maze = Maze(largeur, longueur)
    maze.init_labyrinth()
    maze.init_teleporter()

    screen_size = (vision_radius * 2 + 1) * cell_size
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Génération du Labyrinthe")
    clock = pygame.time.Clock()


    if algorithm == 1:
        if show_gen == "o":
            generation_generator = maze.dfs_generation_animated(0, 0)
            animating = True
            while animating:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                try:
                    state = next(generation_generator)
                    draw_labyrinth(maze, screen, cell_size, state)
                    pygame.display.set_caption("Génération du Labyrinthe")
                    clock.tick(30)
                except StopIteration:
                    animating = False
                    pygame.display.set_caption("Labyrinthe Généré")
                    pygame.time.delay(2000)
        else:
            maze.dfs_generation(0, 0)
        
            draw_labyrinth(maze, screen, cell_size)
    else:
        maze.prim_algo(0, 0)
    if braid == 'o':
        maze.braid_maze(p=0.5)
    optimal_path_length = len(maze.dijkstra(0, 0, maze.width-1, maze.height-1))


    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("The Ultimate Maze")
    clock = pygame.time.Clock()

    player_pos = [0.0, 0.0]
    move_count = 0
    traveled_path = [tuple(player_pos)]
    next_wall_trigger = 5 if difficulty == 3 else None

    tps = maze.get_tp()
    help_path = None
    aide = 0

    key_moves = {
        pygame.K_UP: (0, -1, 'UP'),
        pygame.K_DOWN: (0, 1, 'DOWN'),
        pygame.K_LEFT: (-1, 0, 'LEFT'),
        pygame.K_RIGHT: (1, 0, 'RIGHT')
    }


    with_pacman = (pacman_choice == "o")
    if with_pacman:
        pacman_pos = [maze.width - 1, maze.height - 1] 
        pacman_update_counter = 0
        pacman_update_interval = 30 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key in key_moves:
                    dx, dy, direction = key_moves[event.key]
                    if can_move(maze, int(player_pos[0]), int(player_pos[1]), direction):
                        new_pos = [player_pos[0] + dx, player_pos[1] + dy]
                        animate_movement(maze, player_pos, new_pos, screen, cell_size, vision_radius, wall_color, clock)
                        player_pos = new_pos
                        move_count += 1
                        traveled_path.append(tuple(player_pos))
                        help_path = None
                if event.key == pygame.K_q and aide <= 2:
                    help_path = maze.dijkstra(int(player_pos[0]), int(player_pos[1]), maze.width-1, maze.height-1)
                    aide += 1
                if event.key == pygame.K_TAB:
                    path = maze.dijkstra(int(player_pos[0]), int(player_pos[1]), maze.width-1, maze.height-1)
                    if path:
                        for next_pos in path[1:]:
                            animate_movement(maze, player_pos, next_pos, screen, cell_size, vision_radius, wall_color, clock)
                            player_pos = [float(next_pos[0]), float(next_pos[1])]
                            move_count += 1
                            traveled_path.append(tuple(player_pos))
                        help_path = None

        if difficulty == 3 and move_count >= next_wall_trigger:
            maze.add_random_wall(int(player_pos[0]), int(player_pos[1]))
            next_wall_trigger += 5

    
        if with_pacman:
            pacman_update_counter += 1
            if pacman_update_counter >= pacman_update_interval:
                path = maze.dijkstra(int(pacman_pos[0]), int(pacman_pos[1]), int(player_pos[0]), int(player_pos[1]))
                if path and len(path) > 1:
                    next_step = path[1]
                    pacman_pos = [next_step[0], next_step[1]]
                    if (int(pacman_pos[0]), int(pacman_pos[1])) == (int(player_pos[0]), int(player_pos[1])):
                        print("Pacman vous a attrapé ! Vous revenez au début.")
                        player_pos = [0.0, 0.0]
                        move_count += 1
                        traveled_path = [tuple(player_pos)]
                pacman_update_counter = 0

        if maze.is_end(int(player_pos[0]), int(player_pos[1])):
            optimal_moves = len(maze.dijkstra(0, 0, maze.width-1, maze.height-1)) - 1 if maze.dijkstra(0, 0, maze.width-1, maze.height-1) else None
            print("Mouvements réalisés :", move_count)
            print("Nombre de mouvements du chemin optimal :", optimal_path_length)
            if optimal_path_length is not None and move_count <= optimal_path_length:
                print("Vous avez pris le plus court chemin")
            else:
                print("Vous n'avez pas pris le chemin le plus court")
            exit_maze(screen, maze, player_pos, cell_size, vision_radius, wall_color, 'RIGHT')
            display_message(screen, "Bravo ! Vous avez gagné !", 36, COLOR_MESSAGE, (150, 150))
            pygame.display.flip()
            pause_game(screen)
            running = False

        if maze.is_tp(int(player_pos[0]), int(player_pos[1])):
            if (int(player_pos[0]), int(player_pos[1])) == tps[0]:
                player_pos[0], player_pos[1] = tps[1]
            else:
                player_pos[0], player_pos[1] = tps[0]
            maze.remove_tps()
            move_count += 1
            traveled_path.append(tuple(player_pos))
            help_path = None

        screen.fill(COLOR_BG)
        draw_maze(maze, screen, cell_size, player_pos, vision_radius, wall_color, help_path, traveled_path)
        center = vision_radius * cell_size
        pygame.draw.rect(screen, COLOR_PLAYER, (center + 3, center + 3, cell_size - 6, cell_size - 6))
        if with_pacman:
            base_x = int(player_pos[0])
            base_y = int(player_pos[1])
            offset_x = (player_pos[0] - base_x) * cell_size
            offset_y = (player_pos[1] - base_y) * cell_size
            pacman_pixel_x = (pacman_pos[0] - base_x + vision_radius) * cell_size - offset_x + cell_size // 2
            pacman_pixel_y = (pacman_pos[1] - base_y + vision_radius) * cell_size - offset_y + cell_size // 2
            pygame.draw.circle(screen, COLOR_PACMAN, (int(pacman_pixel_x), int(pacman_pixel_y)), cell_size // 2)
        pygame.display.flip()
        clock.tick(70)
    pygame.quit()

if __name__ == "__main__":
    """la fonction main
    """
    params = get_game_parameters()
    seed_input = params["seed"]
    if seed_input:
        try:
            seed_value = int(seed_input)
        except Exception:
            seed_value = hash(seed_input)
        mz.rnd.seed(seed_value)
    else:
        generated_seed = random.randint(0, 10**12)
        print("Seed générée automatiquement:", generated_seed)
        mz.rnd.seed(generated_seed)
    main(params["difficulty"], params["algorithm"], params["largeur"], params["longueur"], params["braid"],params["show_gen"],params["pacman"])
