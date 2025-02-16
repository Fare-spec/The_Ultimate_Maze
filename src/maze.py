import pickle
import random as rnd
import pile as lifo
import heapq

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def init_labyrinth(self):
        self.grille = [
            [
                {
                    'visited': False,
                    'walls': {'N': True, 'S': True, 'E': True, 'W': True},
                    'teleporter': False,
                }
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

    def init_teleporter(self):
        x, y = rnd.randint(0, self.width-1), rnd.randint(0, self.height-1)
        x2, y2 = rnd.randint(0, self.width-1), rnd.randint(0, self.height-1)
        self.grille[y][x]['teleporter'] = True
        self.grille[y2][x2]['teleporter'] = True

    def is_tp(self, x, y):
        return self.grille[y][x]['teleporter']

    def is_end(self, x, y):
        return (y == self.height - 1 and x == self.width - 1)

    def get_tp(self):
        tp = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grille[y][x]['teleporter']:
                    tp.append((x, y))
        return tp

    def remove_tps(self):
        for y in range(self.height):
            for x in range(self.width):
                self.grille[y][x]['teleporter'] = False
        return self

    def get_unvisited(self):
        cells_unvisited = [(x, y) for y in range(self.height) for x in range(self.width) if not self.grille[y][x]['visited']]
        return cells_unvisited

    def delete_wall(self, x, y, direction):
        self.grille[y][x]['walls'][direction] = False

    def get_voisins(self, x, y):
        voisins = []
        if x > 0: voisins.append((x - 1, y))
        if x < self.width - 1: voisins.append((x + 1, y))
        if y > 0: voisins.append((x, y - 1))
        if y < self.height - 1: voisins.append((x, y + 1))
        return voisins

    def is_visited(self, x, y):
        return self.grille[y][x]['visited']

    def identify_direction(self, x1, y1, x2, y2):
        if x1 == x2:
            return ('N', 'S') if y1 > y2 else ('S', 'N')
        return ('W', 'E') if x1 > x2 else ('E', 'W')

    def dfs_generation(self, x_debut, y_debut):
        self.grille[self.height - 1][self.width - 1]['walls']['E'] = False
        self.grille[y_debut][x_debut]['visited'] = True
        chemin = lifo.creer_pile_vide()
        chemin = lifo.empiler(chemin, (x_debut, y_debut))

        while not lifo.est_pile_vide(chemin):
            current = lifo.sommet(chemin)
            unvisited = [v for v in self.get_voisins(*current) if not self.is_visited(*v)]

            if unvisited:
                selected_voisin = rnd.choice(unvisited)
                murs = self.identify_direction(*current, *selected_voisin)
                self.delete_wall(*current, murs[0])
                self.delete_wall(*selected_voisin, murs[1])
                self.grille[selected_voisin[1]][selected_voisin[0]]['visited'] = True
                chemin = lifo.empiler(chemin, selected_voisin)
            else:
                chemin = lifo.depiler(chemin)

    def prim_algo(self, x_debut, y_debut):
        self.grille[self.height - 1][self.width - 1]['walls']['E'] = False
        self.grille[y_debut][x_debut]['visited'] = True
        frontier = self.get_voisins(x_debut, y_debut)

        while frontier:
            x, y = rnd.choice(frontier)
            visited_neighbors = [v for v in self.get_voisins(x, y) if self.is_visited(*v)]
            if visited_neighbors:
                cell2 = rnd.choice(visited_neighbors)
                wall1, wall2 = self.identify_direction(x, y, *cell2)
                self.delete_wall(x, y, wall1)
                self.delete_wall(*cell2, wall2)
            self.grille[y][x]['visited'] = True
            frontier.remove((x, y))
            for voisin in self.get_voisins(x, y):
                if not self.is_visited(*voisin) and voisin not in frontier:
                    frontier.append(voisin)

    def dijkstra(self,x_start,y_start):
        distances = {(x, y): float('inf') for y in range(self.height) for x in range(self.width)}
        distances[(x_start,y_start)] = 0
        precedent = {}
        queue = [(0, (x_start, y_start))]
        while queue:
            current, (x,y) = heapq.heappop(queue)
            if self.is_end(x,y):
                path = []
                while (x,y) in precedent:
                    path.append((x,y))
                    x, y = precedent[(x,y)]
                path.append((x_start,y_start))
                path.reverse()
                return path
            for x2,y2 in self.get_voisins(x,y):
                direction = self.identify_direction(x, y, x2, y2)[0]
                if not self.grille[y][x]['walls'][direction]:
                    new_dist = current+1
                    if new_dist<distances[(x2,y2)]:
                        distances[(x2,y2)] = new_dist
                        precedent[(x2,y2)] = (x,y)
                        heapq.heappush(queue, (new_dist,(x2,y2)))
        return None




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
    width = input("Entrer la taille en largeur du labyrinthe: ")
    height = input("Entrer la taille en longueur du labyrinthe: ")
    if seed == "":
        seed = rnd.randint(1, 100000000000000)
        print(f"Seed: {seed}")
    rnd.seed(seed)

    maze = generate_and_print_labyrinth(int(width), int(height), 0, 0)

    chemin = maze.dijkstra(0,0)
    print(chemin)

    save_choice = input("Voulez-vous enregistrer le labyrinthe ? (o/n) : ")
    if save_choice.lower() == 'o':
        filename = input("Entrez le nom du fichier (ex: labyrinthe.bin) : ")
        with open(filename, "wb") as file:
            pickle.dump(maze, file)
        print(f"Labyrinthe enregistré sous {filename}")

