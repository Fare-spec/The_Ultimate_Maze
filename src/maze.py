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
        x, y = rnd.randint(1, self.width-1), rnd.randint(1, self.height-1)
        x2, y2 = rnd.randint(1, self.width-1), rnd.randint(1, self.height-1)
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
    def dfs_generation_animated(self, x_debut, y_debut):
        self.grille[self.height - 1][self.width - 1]['walls']['E'] = False
        self.grille[y_debut][x_debut]['visited'] = True
        chemin = lifo.creer_pile_vide()
        chemin = lifo.empiler(chemin, (x_debut, y_debut))
        yield {"current": (x_debut, y_debut), "stack": list(chemin), "maze": self.grille}
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
            yield {"current": current, "stack": list(chemin), "maze": self.grille}

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

    def dijkstra(self, x_start, y_start, x_end, y_end, tp_penalty=1):
        import math, heapq
        dist = {}
        pred = {}
        for y in range(self.height):
            for x in range(self.width):
                dist[(x, y, True)] = math.inf
                dist[(x, y, False)] = math.inf
        start_state = (x_start, y_start, True)
        dist[start_state] = 0
        pq = [(0, start_state)]
        
        TP = self.get_tp()

        while pq:
            d, state = heapq.heappop(pq)
            if d > dist[state]:
                continue
            x, y, tp_avail = state
            if (x, y) == (x_end, y_end):
                path = []
                cur = state
                while cur in pred:
                    path.append((cur[0], cur[1]))
                    cur = pred[cur][0]
                path.append((x_start, y_start))
                path.reverse()
                return path

            if tp_avail and self.grille[y][x]['teleporter']:
                for (tx, ty) in TP:
                    if (tx, ty) != (x, y):
                        new_state = (tx, ty, False)
                        nd = d + tp_penalty
                        if nd < dist[new_state]:
                            dist[new_state] = nd
                            pred[new_state] = (state, 'teleport')
                            heapq.heappush(pq, (nd, new_state))
                continue

            for (nx, ny) in self.get_voisins(x, y):
                direction = self.identify_direction(x, y, nx, ny)[0]
                if not self.grille[y][x]['walls'][direction]:
                    if tp_avail and self.grille[ny][nx]['teleporter']:
                        base_cost = d + 1
                        for (tx, ty) in TP:
                            if (tx, ty) != (nx, ny):
                                new_state = (tx, ty, False)
                                nd = base_cost + tp_penalty
                                if nd < dist[new_state]:
                                    dist[new_state] = nd
                                    pred[new_state] = (state, 'teleport')
                                    heapq.heappush(pq, (nd, new_state))
                    else:
                        new_state = (nx, ny, tp_avail)
                        nd = d + 1
                        if nd < dist[new_state]:
                            dist[new_state] = nd
                            pred[new_state] = (state, 'normal')
                            heapq.heappush(pq, (nd, new_state))
        return None


    def braid_maze(self, p=0.5):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grille[y][x]
                open_passages = sum(1 for ouvert in cell['walls'].values() if not ouvert)
                if open_passages == 1:
                    closed_walls = []
                    for direction, ouvert in cell['walls'].items():
                        if ouvert:
                            if (direction == 'N' and y == 0) or \
                            (direction == 'S' and y == self.height - 1) or \
                            (direction == 'W' and x == 0) or \
                            (direction == 'E' and x == self.width - 1):
                                continue

                            voisin = None
                            if direction == 'N' and y > 0:
                                voisin = self.grille[y-1][x]
                            elif direction == 'S' and y < self.height - 1:
                                voisin = self.grille[y+1][x]
                            elif direction == 'W' and x > 0:
                                voisin = self.grille[y][x-1]
                            elif direction == 'E' and x < self.width - 1:
                                voisin = self.grille[y][x+1]
                            if voisin is not None:
                                open_voisin = sum(1 for o in voisin['walls'].values() if not o)
                                if open_voisin > 1:
                                    closed_walls.append(direction)
                    if closed_walls and rnd.random() < p:
                        mur_choisi = rnd.choice(closed_walls)
                        cell['walls'][mur_choisi] = False
                        if mur_choisi == 'N' and y > 0:
                            self.grille[y-1][x]['walls']['S'] = False
                        elif mur_choisi == 'S' and y < self.height - 1:
                            self.grille[y+1][x]['walls']['N'] = False
                        elif mur_choisi == 'W' and x > 0:
                            self.grille[y][x-1]['walls']['E'] = False
                        elif mur_choisi == 'E' and x < self.width - 1:
                            self.grille[y][x+1]['walls']['W'] = False


    def add_random_wall(self,xg,yg):
        candidate_cells = []
        for y in range(self.height):
            for x in range(self.width):
                for (nx, ny) in self.get_voisins(x, y):
                    d_from, _ = self.identify_direction(x, y, nx, ny)
                    if not self.grille[y][x]['walls'][d_from]:
                        candidate_cells.append((x, y))
                        break
        if not candidate_cells:
            return

        x0, y0 = rnd.choice(candidate_cells)

        connected_neighbors = []
        for (nx, ny) in self.get_voisins(x0, y0):
            d_from, _ = self.identify_direction(x0, y0, nx, ny)
            if not self.grille[y0][x0]['walls'][d_from]:
                connected_neighbors.append((nx, ny))

        if not connected_neighbors:
            return

        nx, ny = rnd.choice(connected_neighbors)
        d_from, d_to = self.identify_direction(x0, y0, nx, ny)

        self.grille[y0][x0]['walls'][d_from] = True
        self.grille[ny][nx]['walls'][d_to] = True

        if self.dijkstra(xg,yg) == 1 or self.dijkstra(xg,yg) is None:
            self.grille[y0][x0]['walls'][d_from] = False
            self.grille[ny][nx]['walls'][d_to] = False
            self.braid_maze()









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
        seed = rnd.randint(1, 10**12)
        print(f"Seed: {seed}")
    rnd.seed(seed)

    maze = generate_and_print_labyrinth(int(width), int(height), 0, 0)

    chemin = maze.dijkstra(0,0,maze.width-1,maze.height-1)
    print(chemin)

    save_choice = input("Voulez-vous enregistrer le labyrinthe ? (o/n) : ")
    if save_choice.lower() == 'o':
        filename = input("Entrez le nom du fichier (ex: labyrinthe.bin) : ")
        with open(filename, "wb") as file:
            pickle.dump(maze, file)
        print(f"Labyrinthe enregistré sous {filename}")