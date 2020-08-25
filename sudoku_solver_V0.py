import numpy as np
import Old_Tile as Tile

# V0 - Solves with backtracking iteration. No UI

def make_grid(grid):
    for i in range(9):
        row = []
        for j in range(9):
            tile = Tile.Tile(None, i, j, 1)
            row.append(tile)
        grid.append(row)

    return grid


def issue_with_tile(grid, my_tile):
    issue = False

    # check non blank
    if not my_tile.num:
        return issue

    # check row
    for tile in grid[my_tile.row]:
        if tile.num == my_tile.num and tile.col != my_tile.col:
            issue = True
            return issue

    # check col
    column = [row[my_tile.col] for row in grid]

    for tile in column:
        if tile.num == my_tile.num and tile.row != my_tile.row:
            issue = True
            return issue

    # check square
    for i in range((my_tile.row // 3) * 3, (my_tile.row // 3) * 3 + 3):
        for j in range((my_tile.col // 3 * 3), (my_tile.col // 3) * 3 + 3):
            if grid[i][j].num == my_tile.num and grid[i][j] != my_tile:
                issue = True
                return issue

    return issue


def print_grid(grid):
    G = np.empty([9, 9])

    for row in grid:
        for tile in row:
            if tile.num:
                G[tile.row][tile.col] = tile.num
            else:
                G[tile.row][tile.col] = 0

    print(G)


def get_next(grid, my_tile):
    if my_tile.col < 8:
        return grid[my_tile.row][my_tile.col + 1]
    elif my_tile.row < 8:
        return grid[my_tile.row + 1][0]
    else:   #last tile
        return None


def solve_grid(grid, my_tile):

    solved = False
    n = 1

    while not solved and n <= 9:
        my_tile.set_to(n)
        if my_tile.fixed or not issue_with_tile(grid, my_tile):
            next_tile = get_next(grid, my_tile)
            if not next_tile:   # i am done
                return True
            else:
                print_grid(grid)
                solved = solve_grid(grid, next_tile)

        n += 1

    # clear tile before going back
    if not solved:
        my_tile.clear()

    return solved


sudoku_grid = []
sudoku_grid = make_grid(sudoku_grid)

# tile_1 = sudoku_grid[8][8]
# tile_2 = sudoku_grid[6][6]
# tile_1.num = 1
# tile_2.num = 1
# print_grid(sudoku_grid)
# print(issue_with_tile(sudoku_grid, tile_1))

sudoku_grid[0][0].num = 9
sudoku_grid[0][0].fix()

sudoku_grid[4][4].num = 5
sudoku_grid[4][4].fix()

sudoku_grid[8][8].num = 2
sudoku_grid[8][8].fix()

if solve_grid(sudoku_grid, sudoku_grid[0][0]):
    print_grid(sudoku_grid)
else:
    print("Cannot be solved.")