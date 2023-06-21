import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    ans = []
    for i in range(0, len(values), n):
        ans.append(values[i : i + n])

    return ans


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    ans = []
    for item in grid:
        ans.append(item[pos[1]])

    return ans


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    ans = []
    pos_y = pos[0] // 3 * 3
    pos_x = pos[1] // 3 * 3
    for i in range(pos_y, pos_y + 3):
        for j in range(pos_x, pos_x + 3):
            ans.append(grid[i][j])
    return ans


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Tuple[int, int]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j

    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    possible_values = set("123456789")
    possible_values -= set(get_row(grid, pos))
    possible_values -= set(get_col(grid, pos))
    possible_values -= set(get_block(grid, pos))

    return possible_values


def solve(grid: tp.List[tp.List[str]]):
    empty_position = find_empty_positions(grid)
    if empty_position == (-1, -1):
        return grid
    possible_values = find_possible_values(grid, empty_position)
    for i in possible_values:
        grid[empty_position[0]][empty_position[1]] = i
        new_solve = solve(grid)
        if new_solve:
            return new_solve
    grid[empty_position[0]][empty_position[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    s = set("123456789")
    for i in range(len(solution) // 3):
        for j in range(len(solution) // 3):
            sol = set(get_block(solution, (i * 3, j * 3)))
            if sol != s:
                return False

    for i in range(len(solution)):
        sol = set(solution[i])
        if sol != s:
            return False

    for i in range(len(solution)):
        ss = ""
        for j in range(len(solution)):
            ss += solution[i][j]
        sol = set(ss)
        if sol != s:
            return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["." for i in range(9)] for j in range(9)]
    grid = solve(grid)
    N = N if N <= 81 else 81
    for i in range(81 - N):
        x = randint(0, 8)
        y = randint(0, 8)
        while grid[x][y] == ".":
            x = randint(0, 8)
            y = randint(0, 8)
        grid[x][y] = "."
    return grid


if __name__ == "__main__":
    grid = [
        ["5", "3", ".", ".", "7", ".", ".", ".", "."],
        ["6", ".", ".", "1", "9", "5", ".", ".", "."],
        [".", "9", "8", ".", ".", ".", ".", "6", "."],
        ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
        ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
        ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
        [".", "6", ".", ".", ".", ".", "2", "8", "."],
        [".", ".", ".", "4", "1", "9", ".", ".", "5"],
        [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ]
    print(solve(grid))
