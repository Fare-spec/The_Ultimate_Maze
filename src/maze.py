import liste as fifo
import random as rnd
import pile as lifo
rnd.seed(110)

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init_labyrinth(self):
        self.grille = [
            [
                {
                    'visited': False,
                    'walls': {'N': True, 'S': True, 'E': True, 'W': True}
                }
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]
    def get_unvisited(self):
        cells_unvisited = []
        for y in range(self.height):
            for x in range(self.width):
                if not self.grille[y][x]['visited']:
                    cells_unvisited.append((x, y))
        return cells_unvisited


    def delete_wall(self, x, y, direction):
        self.grille[y][x]['walls'][direction] = False
    

    def get_voisins(self, x, y):
        voisins = []
        if x > 0:
            voisins.append((x - 1, y))
        if x < self.width - 1:
            voisins.append((x + 1, y))
        if y > 0:
            voisins.append((x, y - 1))
        if y < self.height - 1:
            voisins.append((x, y + 1))
        return voisins
    
    def is_visited(self,x,y):
        return self.grille[y][x]['visited']
    

    def identify_direction(self,x1,y1,x2,y2):
        if x1 == x2:
            if y1 == y2+1:
                return 'N','S'
            else:
                return 'S','N'
        elif x1 == x2+1:
            return 'W','E'
        else:
            return 'E','W'


    def dfs_generation(self, x_debut, y_debut):
        self.grille[y_debut][x_debut]['visited'] = True
        chemin = lifo.creer_pile_vide()
        chemin = lifo.empiler(chemin, (x_debut, y_debut))
        while not lifo.est_pile_vide(chemin):
            current = lifo.sommet(chemin)
            voisins = self.get_voisins(current[0], current[1])
            unvisited = [voisin for voisin in voisins if not self.is_visited(voisin[0], voisin[1])]
            if unvisited:
                selected_voisin = rnd.choice(unvisited)
                murs = self.identify_direction(current[0], current[1], selected_voisin[0], selected_voisin[1])
                self.delete_wall(current[0], current[1], murs[0])
                self.delete_wall(selected_voisin[0], selected_voisin[1], murs[1])
                self.grille[selected_voisin[1]][selected_voisin[0]]['visited'] = True
                chemin = lifo.empiler(chemin, selected_voisin)
            else:
                chemin = lifo.depiler(chemin)


def print_labyrinth(maze):
    """
    Affiche le labyrinthe dans la console en utilisant des caractères ASCII.
    Chaque cellule est dessinée en fonction de l'état de ses murs (N, S, E, W).
    """
    # Pour chaque ligne du labyrinthe
    for y in range(maze.height):
        # Première ligne : affiche les murs du haut (Nord)
        top_line = ""
        for x in range(maze.width):
            if maze.grille[y][x]['walls']['N']:
                top_line += "+---"
            else:
                top_line += "+   "
        top_line += "+"
        print(top_line)

        # Deuxième ligne : affiche le mur de gauche (Ouest) et l'intérieur de la cellule
        mid_line = ""
        for x in range(maze.width):
            if maze.grille[y][x]['walls']['W']:
                mid_line += "|   "
            else:
                mid_line += "    "
        # Pour la dernière cellule de la ligne, on vérifie le mur Est
        if maze.grille[y][-1]['walls']['E']:
            mid_line += "|"
        else:
            mid_line += " "
        print(mid_line)
    
    # Affiche la dernière ligne du labyrinthe (murs du bas - Sud)
    bottom_line = ""
    for x in range(maze.width):
        if maze.grille[maze.height - 1][x]['walls']['S']:
            bottom_line += "+---"
        else:
            bottom_line += "+   "
    bottom_line += "+"
    print(bottom_line)


def generate_and_print_labyrinth(width, height, start_x=0, start_y=0):
    """
    Instancie un objet Maze, initialise la grille, génère le labyrinthe avec DFS,
    puis l'affiche via print_labyrinth.
    """
    maze = Maze(width, height)
    maze.init_labyrinth()
    # On marque la cellule de départ comme visitée avant de lancer DFS.
    maze.grille[start_y][start_x]['visited'] = True
    maze.dfs_generation(start_x, start_y)
    print_labyrinth(maze)


# Exemple d'utilisation :
if __name__ == "__main__":
    # Génère un labyrinthe de 10x10 à partir de la cellule (0, 0)
    generate_and_print_labyrinth(10, 10, 0, 0)

