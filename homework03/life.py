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
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:

        grid = []
        for i in range(self.cell_height):
            grid.append([0] * self.cell_width)

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if randomize:
                    grid[i][j] = random.randint(0, 1)
                else:
                    grid[i][j] = 0
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:

        neighbours_cells = []

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if -1 < i < self.cell_height and -1 < j < self.cell_width and cell != (i, j):
                    neighbours_cells.append(self.grid[i][j])
        return neighbours_cells

    def get_next_generation(self) -> Grid:

        new_grid = [row.copy() for row in self.grid]
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours_count = sum(neighbours)

                k = not self.grid[i][j]

                if not self.grid[i][j] and alive_neighbours_count == 3:
                    new_grid[i][j] = 1
                elif self.grid[i][j] and alive_neighbours_count not in (2, 3):
                    new_grid[i][j] = 0

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = (self.get_next_generation(),)
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
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
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(
                "\n".join([" ".join(map(str, self.curr_generation[i])) for i in range(self.rows)])
            )
