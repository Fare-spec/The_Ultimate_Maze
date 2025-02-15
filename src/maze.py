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
        self.grille[y_debut][x_debut]['walls']['W'] = False
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
        self.grille[y_debut][x_debut]['walls']['W'] = False
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
