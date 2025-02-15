import pickle
import random as rnd
import pile as lifo

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

    def is_visited(self, x, y):
        return self.grille[y][x]['visited']

    def identify_direction(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 == y2 + 1:
                return 'N', 'S'
            else:
                return 'S', 'N'
        elif x1 == x2 + 1:
            return 'W', 'E'
        else:
            return 'E', 'W'

    def dfs_generation(self, x_debut, y_debut):

        self.grille[y_debut][x_debut]['walls']['W'] = False
        self.grille[self.width - 1][self.height - 1]['walls']['E'] = False
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
    def prim_algo(self, x_debut, y_debut):
        self.grille[y_debut][x_debut]['walls']['W'] = False
        self.grille[self.width - 1][self.height - 1]['walls']['E'] = False
        self.grille[y_debut][x_debut]['visited'] = True        
        frontier = self.get_voisins(x_debut, y_debut)
        while frontier:
            cell = rnd.choice(frontier)
            x, y = cell[0], cell[1]
            visited_neighbors = [voisin for voisin in self.get_voisins(x, y)if self.is_visited(voisin[0], voisin[1])]
            if visited_neighbors:
                cell2 = rnd.choice(visited_neighbors)
                wall1, wall2 = self.identify_direction(x, y, cell2[0], cell2[1])
                self.delete_wall(x, y, wall1)
                self.delete_wall(cell2[0], cell2[1], wall2)
            self.grille[y][x]['visited'] = True
            frontier.remove(cell)
            for voisin in self.get_voisins(x, y):
                vx, vy = voisin[0], voisin[1]
                if not self.is_visited(vx, vy) and voisin not in frontier:
                    frontier.append(voisin)

def print_labyrinth(maze):
    for y in range(maze.height):
        top_line = ""
        for x in range(maze.width):
            if maze.grille[y][x]['walls']['N']:
                top_line += "+---"
            else:
                top_line += "+   "
        top_line += "+"
        print(top_line)

        mid_line = ""
        for x in range(maze.width):
            if maze.grille[y][x]['walls']['W']:
                mid_line += "|   "
            else:
                mid_line += "    "
        if maze.grille[y][-1]['walls']['E']:
            mid_line += "|"
        else:
            mid_line += " "
        print(mid_line)

    bottom_line = ""
    for x in range(maze.width):
        if maze.grille[maze.height - 1][x]['walls']['S']:
            bottom_line += "+---"
        else:
            bottom_line += "+   "
    bottom_line += "+"
    print(bottom_line)

def generate_and_print_labyrinth(width, height, start_x=0, start_y=0):
    maze = Maze(width, height)
    maze.init_labyrinth()
    maze.grille[start_y][start_x]['visited'] = True
    maze.prim_algo(start_x, start_y)
    print_labyrinth(maze)
    return maze

if __name__ == "__main__":
    seed = input("Entrer une seed ou laisser vide: ")
    width = input("Entrer la taille en largeur du labyrinth: ")
    height = input("Entrer la taille en longueur du labyrinth: ")
    if seed == "":
        seed = rnd.randint(1, 100000000000000)
        print(f"Seed: {seed}")
    rnd.seed(seed)

    maze = generate_and_print_labyrinth(int(width), int(height), 0, 0)

    save_choice = input("Voulez-vous enregistrer le labyrinthe ? (o/n) : ")
    if save_choice.lower() == 'o':
        filename = input("Entrez le nom du fichier (ex: labyrinthe.bin) : ")
        with open(filename, "wb") as file:
            pickle.dump(maze, file)
        print(f"Labyrinthe enregistré sous {filename}")

