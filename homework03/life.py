import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:

        grid = []
        for i in range(self.cols):
            grid.append([0] * self.rows)

        for i in range(self.cols):
            for j in range(self.rows):
                if randomize:
                    grid[i][j] = random.randint(0, 1)
                else:
                    grid[i][j] = 0
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:

        neighbours_cells = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if -1 < i < self.cols and -1 < j < self.rows and cell != (i, j):
                    neighbours_cells.append(self.curr_generation[i][j])
        return neighbours_cells

    def get_next_generation(self) -> Grid:

        new_grid = [row.copy() for row in self.grid]
        for i in range(self.cols):
            for j in range(self.rows):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours_count = sum(neighbours)

                k = not self.grid[i][j]

                if not self.grid[i][j] and alive_neighbours_count == 3:
                    new_grid[i][j] = 1
                elif self.grid[i][j] and alive_neighbours_count not in (2, 3):
                    new_grid[i][j] = 0

        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = (self.get_next_generation(),)
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename) as f:
            grid = []
            width = 0
            height = 0
            for i, line in enumerate(f):
                height += 1
                els = list(map(int, line.split()))
                if not width:
                    width = len(els)
                assert len(els) == width, "Неверный ввод! Различная длина строк"
                grid.append(els)
        game = GameOfLife((height, width))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                "\n".join([" ".join(map(str, self.curr_generation[i])) for i in range(self.rows)])
            )

if __name__ == "__main__":
    grid = [
        [1, 1, 0, 0, 1, 1, 1, 1],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1],
    ]
    rows = 6
    cols = 8
    game = GameOfLife((rows, cols))
    game.curr_generation = grid
    neighbours = game.get_neighbours((2, 0))
    print(neighbours)
