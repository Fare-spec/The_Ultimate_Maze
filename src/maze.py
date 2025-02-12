import liste as fifo
import random as rnd
import pile as lifo
rnd.seed(11)

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


a = Maze(10,10)
a.init_labyrinth()
a.delete_wall(5,5,'N')
b = a.is_visited(0,0)
print(b)
