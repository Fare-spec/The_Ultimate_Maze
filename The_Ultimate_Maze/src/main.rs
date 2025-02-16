use rand::seq::IndexedRandom;
use std::{collections::HashMap, fs::File};
mod pile;
use pile::Stack;

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct Cell {
    visited: bool,
    walls: HashMap<char, bool>,
    teleporter: bool,
}

#[derive(Debug, serde::Serialize, serde::Deserialize)]
struct Maze {
    grille: Vec<Vec<Cell>>,
    width: usize,
    height: usize,
}

impl Maze {
    fn new(width: usize, height: usize) -> Maze {
        let grille = (0..height)
            .map(|_| {
                (0..width)
                    .map(|_| {
                        let mut walls = HashMap::new();
                        walls.insert('N', true);
                        walls.insert('S', true);
                        walls.insert('E', true);
                        walls.insert('W', true);
                        Cell {
                            visited: false,
                            walls,
                            teleporter: false,
                        }
                    })
                    .collect()
            })
            .collect();
        Maze {
            grille,
            width,
            height,
        }
    }
    pub fn identify_direction(&self, x1: usize, y1: usize, x2: usize, y2: usize) -> (char, char) {
        if x1 == x2 {
            if y1 > y2 {
                ('N', 'S')
            } else {
                ('S', 'N')
            }
        } else if x1 > x2 {
            ('W', 'E')
        } else {
            ('E', 'W')
        }
    }

    pub fn set_wall(&mut self, x: usize, y: usize, direction: char, state: bool) {
        if let Some(cell) = self.grille.get_mut(y).and_then(|row| row.get_mut(x)) {
            cell.walls.insert(direction, state);
        }
    }

    fn display(&self) {
        for y in 0..self.height {
            let mut top_line = String::new();
            let mut mid_line = String::new();

            for x in 0..self.width {
                top_line.push_str(if self.grille[y][x].walls[&'N'] {
                    "+---"
                } else {
                    "+   "
                });
                mid_line.push_str(if self.grille[y][x].walls[&'W'] {
                    "|   "
                } else {
                    "    "
                });
            }
            top_line.push('+');
            mid_line.push('|');

            println!("{}", top_line);
            println!("{}", mid_line);
        }

        let mut bottom_line = String::new();
        for x in 0..self.width {
            bottom_line.push_str(if self.grille[self.height - 1][x].walls[&'S'] {
                "+---"
            } else {
                "+   "
            });
        }
        bottom_line.push('+');
        println!("{}", bottom_line);
    }

    fn dfs_generation(&mut self, start_x: usize, start_y: usize) {
        let mut stack = Stack::new();
        stack.push((start_x, start_y));
        self.grille[start_y][start_x].visited = true;

        while !stack.is_empty() {
            let (x, y) = stack.pop().unwrap();
            let neighbors = self.get_unvisited_neighbors(x, y);

            if let Some(&(nx, ny)) = neighbors.choose(&mut rand::rng()) {
                self.remove_wall(x, y, nx, ny);
                self.grille[ny][nx].visited = true;
                stack.push((x, y));
                stack.push((nx, ny));
            }
        }
    }

    pub fn prim_algo(&mut self, x_debut: usize, y_debut: usize) {
        self.grille[y_debut][x_debut].walls.insert('W', false);
        self.grille[self.height - 1][self.width - 1]
            .walls
            .insert('E', false);
        self.grille[y_debut][x_debut].visited = true;
        let mut frontier = self.get_neighbors(x_debut, y_debut);

        let mut rng = rand::rng();
        while !frontier.is_empty() {
            let &(x, y) = frontier.choose(&mut rng).unwrap();
            let visited_neighbors: Vec<(usize, usize)> = self
                .get_neighbors(x, y)
                .into_iter()
                .filter(|&(nx, ny)| self.grille[ny][nx].visited)
                .collect();

            if let Some(&(nx, ny)) = visited_neighbors.choose(&mut rng) {
                let (wall1, wall2) = self.identify_direction(x, y, nx, ny);
                self.set_wall(x, y, wall1, false);
                self.set_wall(nx, ny, wall2, false);
            }
            self.grille[y][x].visited = true;
            frontier.retain(|&(fx, fy)| !(fx == x && fy == y));
            for voisin in self.get_neighbors(x, y) {
                if !self.grille[voisin.1][voisin.0].visited && !frontier.contains(&voisin) {
                    frontier.push(voisin);
                }
            }
        }
    }

    fn get_neighbors(&self, x: usize, y: usize) -> Vec<(usize, usize)> {
        let mut neighbors = vec![];
        if x > 0 {
            neighbors.push((x - 1, y));
        }
        if x < self.width - 1 {
            neighbors.push((x + 1, y));
        }
        if y > 0 {
            neighbors.push((x, y - 1));
        }
        if y < self.height - 1 {
            neighbors.push((x, y + 1));
        }
        neighbors
    }

    fn get_unvisited_neighbors(&self, x: usize, y: usize) -> Vec<(usize, usize)> {
        self.get_neighbors(x, y)
            .into_iter()
            .filter(|&(nx, ny)| !self.grille[ny][nx].visited)
            .collect()
    }

    fn remove_wall(&mut self, x1: usize, y1: usize, x2: usize, y2: usize) {
        if x1 == x2 {
            if y1 > y2 {
                self.grille[y1][x1].walls.insert('N', false);
                self.grille[y2][x2].walls.insert('S', false);
            } else {
                self.grille[y1][x1].walls.insert('S', false);
                self.grille[y2][x2].walls.insert('N', false);
            }
        } else {
            if x1 > x2 {
                self.grille[y1][x1].walls.insert('W', false);
                self.grille[y2][x2].walls.insert('E', false);
            } else {
                self.grille[y1][x1].walls.insert('E', false);
                self.grille[y2][x2].walls.insert('W', false);
            }
        }
    }
    fn save_to_file(&self, filename: &str) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(filename)?;
        bincode::serialize_into(file, self)?;
        Ok(())
    }
}

fn main() {
    let mut maze = Maze::new(20, 20);
    maze.prim_algo(0, 0);
    maze.display();
    println!("Done");
    match maze.save_to_file("maze.bin") {
        Ok(_) => println!("labyrinthe enregistre avec succes."),
        Err(e) => eprintln!("erreur lors de l'enregistrement : {}", e),
    }
}
