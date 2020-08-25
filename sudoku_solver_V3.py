import numpy as np
import Sudoku as Sudoku
import pygame as pygame
import colors as colors
import Button as Button


# V0 - Solves with backtracking iteration. No UI
# V1 - Solves with backtracking iteration. Bug fixed where algo backtracks to fixed tile. Working UI, no buttons
# V2 - Solves with backtracking iteration. Button class, draw_list, Tile inherits from Button
# V3 - Solves with backtracking iteration. Tiles clickable for assigning value. Cluster object, start button, _
# reset button.


def solve_grid(win, grid, my_tile):
    solved = False
    n = 1

    next_tile = grid.get_next(my_tile)

    while not solved and n <= 9:
        my_tile.set_to(n)
        my_tile.draw(win)
        pygame.display.update()

        if my_tile.fixed or not grid.issue_with_tile(my_tile):
            if not next_tile:  # i am done
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


def draw(win, d_list):
    win.fill(colors.WHITE)

    for obt in d_list:
        obt.draw(win)

    pygame.display.update()


def fix_tile_in_grid(grid, num, row, col):
    grid.tiles[row][col].set_to(num)
    grid.tiles[row][col].fix()


pygame.init()
pygame.font.init()
pygame.display.init()

sudoku_width = 360
display_width = 500
display_height = sudoku_width

sudoku_grid = Sudoku.Grid(sudoku_width, colors.SUD_YELLOW, 9)
sudoku_grid.set_values()

fix_tile_in_grid(sudoku_grid, 9, 0, 0)
fix_tile_in_grid(sudoku_grid, 4, 1, 7)
fix_tile_in_grid(sudoku_grid, 5, 4, 4)
fix_tile_in_grid(sudoku_grid, 3, 2, 2)
fix_tile_in_grid(sudoku_grid, 4, 7, 0)
fix_tile_in_grid(sudoku_grid, 2, 8, 8)

win = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Sudoku Solver")

draw_list = []
draw_list.append(sudoku_grid)

button_cluster = Button.ButtonCluster(pygame.Rect((sudoku_width, 0), (display_width - sudoku_width, display_height)),
                                      colors.WHITE, False, False)

button_width = round((display_width - sudoku_width) * 0.7)
button_height = round(button_width * 0.7)
start_button = Button.Button(colors.SUD_YELLOW, pygame.Rect((380, 50), (button_width, button_height)),
                             "START", pygame.font.SysFont("Arial", round(button_height * 0.5)),
                             lambda: solve_grid(win, sudoku_grid, sudoku_grid.tiles[0][0]))

reset_button = start_button.copy()
reset_button.set_string("RESET")
reset_button.set_click_function(lambda: sudoku_grid.reset())

clear_button = reset_button.copy()
clear_button.set_string("CLEAR")
clear_button.set_click_function(lambda: sudoku_grid.clear())

button_cluster.add_button(start_button)
button_cluster.add_button(reset_button)
button_cluster.add_button(clear_button)

draw_list.append(button_cluster)

quit_command = False

while not quit_command:
    draw(win, draw_list)
    for event in pygame.event.get():
        quit_command = event.type == pygame.QUIT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                solve_grid(win, sudoku_grid, sudoku_grid.tiles[0][0])
            elif pygame.K_1 <= event.key <= pygame.K_9:
                if sudoku_grid.tile_selected:
                    sudoku_grid.tile_selected.set_to(int(pygame.key.name(event.key)))
                    sudoku_grid.tile_selected.fix()
                    sudoku_grid.tile_clicked(sudoku_grid.tile_selected)  # virtually cancel selection
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in button_cluster.button_list:
                if button.clicked(event.pos):
                    button.click()

            for row in sudoku_grid.tiles:
                for tile in row:
                    if tile.clicked(event.pos):
                        sudoku_grid.tile_clicked(tile)

pygame.quit()
