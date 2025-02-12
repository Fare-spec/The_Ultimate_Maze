import liste as fifo
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
    
    def is_visited(self,x,y):
        return self.grille[y][x]['visited']



    def dfs_generation(self, x_debut, y_debut):
        chemin = lifo.creer_pile_vide()
        chemin = lifo.empiler(chemin, (x_debut,y_debut))
        while not lifo.est_pile_vide(chemin):
            voisins = self.get_voisins(x_debut, y_debut)
            unvisited = []
            for i in voisins:
                if not self.is_visited(i[0],i[1]):
                    unvisited.append(i)
            rnd.choice(unvisited)


a = Maze(10,10)
a.init_labyrinth()
a.delete_wall(5,5,'N')
b = a.is_visited(0,0)
print(b)
