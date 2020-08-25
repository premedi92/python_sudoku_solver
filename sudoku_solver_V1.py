import numpy as np
import Old_Tile as Tile
import pygame as pygame
import colors as colors

# V0 - Solves with backtracking iteration. No UI
# V1 - Solves with backtracking iteration. Bug fixed where algo backtracks to fixed tile. Working UI, no buttons


def make_grid(grid, grid_width):
    for i in range(9):
        row = []
        for j in range(9):
            tile = Tile.Tile(None, i, j, grid_width // 9)
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


def solve_grid(win, grid, my_tile):

    solved = False
    n = 1

    next_tile = get_next(grid, my_tile)

    while not solved and n <= 9:
        my_tile.set_to(n)
        my_tile.draw(win)
        pygame.display.update()

        if my_tile.fixed or not issue_with_tile(grid, my_tile):
            if not next_tile:   # i am done
                return True
            elif my_tile.fixed:
                return solve_grid(win, grid, next_tile)
                # print_grid(grid)  # debug statements
            else:
                solved = solve_grid(win, grid, next_tile)

        n += 1

    # clear tile before going back
    if not solved:
        my_tile.clear()
        my_tile.draw(win, False)
        pygame.display.update()

    return solved


def draw(win, sudoku_grid):
    win.fill(colors.WHITE)

    for row in sudoku_grid:
        for tile in row:
            tile.draw(win, False)

    pygame.display.update()


def fix_tile_in_grid(grid, num, row, col):
    grid[row][col].num = num
    grid[row][col].fix()


sudoku_width = 360

sudoku_grid = []
sudoku_grid = make_grid(sudoku_grid, sudoku_width)

fix_tile_in_grid(sudoku_grid, 9, 0, 0)
fix_tile_in_grid(sudoku_grid, 4, 1, 7)
fix_tile_in_grid(sudoku_grid, 5, 4, 4)
fix_tile_in_grid(sudoku_grid, 3, 2, 2)
fix_tile_in_grid(sudoku_grid, 4, 7, 0)
fix_tile_in_grid(sudoku_grid, 2, 8, 8)

pygame.init()
pygame.font.init()
pygame.display.init()

display_width = sudoku_width
display_height = sudoku_width

win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Sudoku Solver")

quit_command = False

while not quit_command:
    draw(win, sudoku_grid)
    for event in pygame.event.get():
        quit_command = event.type == pygame.QUIT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                solve_grid(win, sudoku_grid, sudoku_grid[0][0])

pygame.quit()