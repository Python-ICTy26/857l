import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

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

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                value = self.grid[i][j]
                color = pygame.Color("green") if value else pygame.Color("white")
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(
                        j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size
                    ),
                )
        return None

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


if __name__ == "__main__":
    game = GameOfLife(1000, 525, 25, 10)
    game.run()
