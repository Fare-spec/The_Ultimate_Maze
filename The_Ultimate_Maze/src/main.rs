use std::collections::HashMap;
mod pile;
#[derive(Debug)]
struct Cell {
    visited: bool,
    walls: HashMap<char, bool>,
}

#[derive(Debug)]
struct Maze {
    grille: Vec<Vec<Cell>>,
    width: usize,
    height: usize,
}

impl Maze {
    fn new(height: usize, width: usize) -> Maze {
        let grille: Vec<Vec<Cell>> = (0..height)
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
}

fn main() {
    let maze = Maze::new(5, 5);
    println!("{:#?}", maze);
}
