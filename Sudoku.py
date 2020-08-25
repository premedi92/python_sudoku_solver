import pygame as pygame
import colors as colors
import Button as Button
import numpy as numpy


class Tile(Button.Button):
    def __init__(self, color, rect, string, font, click_function):
        super().__init__(color, rect, string, font, click_function)
        self.row = self.rect.y // self.rect.height
        self.col = self.rect.x // self.rect.width
        self.selected = False
        try:
            self.num = int(self.string)
        except ValueError:
            self.num = None
        self.fixed = False

    def set_to(self, num):
        if not self.fixed:
            self.num = num
            self.string = str(num)

    def clear(self):
        if not self.fixed:
            self.num = None
            self.string = ""

    def unfix(self):
        self.fixed = False

    def fix(self):
        self.fixed = True

    def is_last(self):
        return self.row == 8 and self.col == 8

    def draw(self, win, fast=True):
        if not fast:
            pygame.draw.rect(win, self.color, self.rect)
            pygame.draw.rect(win, colors.BLACK, self.rect, 1)

        if self.num:
            if self.fixed:
                num_color = colors.RED
            else:
                num_color = colors.BLACK
            w, h = self.font.size(str(self.num))
            num = self.font.render(str(self.num), True, num_color, self.color)
            win.blit(num, numpy.subtract(self.rect.center, (w // 2, h // 2)))

    def click(self):
        self.selected = not self.selected

        if self.selected:
            self.color = colors.SUD_BLUE
            self.unfix()
            self.clear()
        else:
            self.color = colors.SUD_YELLOW


class Grid:
    def __init__(self, width, color, tiles_per_row=9):
        self.width = width
        self.color = color
        self.tiles_per_row = tiles_per_row
        self.tiles = []
        self.tile_selected = None

        for i in range(self.tiles_per_row):
            row = []
            for j in range(self.tiles_per_row):
                tile_width = self.width // self.tiles_per_row
                tile = Tile(self.color, pygame.Rect((j * tile_width, i * tile_width), (tile_width, tile_width)),
                            "", pygame.font.SysFont("Arial", round(tile_width * 0.5)), None)
                row.append(tile)
            self.tiles.append(row)

    def reset(self):
        for row in self.tiles:
            for tile in row:
                tile.clear()

    def clear(self):
        for row in self.tiles:
            for tile in row:
                tile.unfix()
                tile.clear()

    def set_values(self, *args):

        # make sure args is a tiles_per_row x tiles_per_row list
        if type(args) == list:
            args_2 = [row for row in args if len(row) == self.tiles_per_row]    # load rows with tiles_per_row elements
            if len(args) == len(args_2) and len(args) == self.tiles_per_row:    # compare
                for i in range(self.tiles_per_row):
                    for j in range(self.tiles_per_row):
                        self.tiles[i][j].set_to(args[i][j])

    def issue_with_tile(self, my_tile):
        issue = False

        # check non blank
        if not my_tile.num:
            return issue

        # check row
        for tile in self.tiles[my_tile.row]:
            if tile.num == my_tile.num and tile.col != my_tile.col:
                issue = True
                return issue

        # check col
        column = [row[my_tile.col] for row in self.tiles]

        for tile in column:
            if tile.num == my_tile.num and tile.row != my_tile.row:
                issue = True
                return issue

        # check square
        for i in range((my_tile.row // 3) * 3, (my_tile.row // 3) * 3 + 3):
            for j in range((my_tile.col // 3 * 3), (my_tile.col // 3) * 3 + 3):
                if self.tiles[i][j].num == my_tile.num and self.tiles[i][j] != my_tile:
                    issue = True
                    return issue

        return issue

    def get_next(self, my_tile):
        if my_tile.col < 8:
            return self.tiles[my_tile.row][my_tile.col + 1]
        elif my_tile.row < 8:
            return self.tiles[my_tile.row + 1][0]
        else:  # last tile
            return None

    def draw(self, win):
        for row in self.tiles:
            for tile in row:
                tile.draw(win, False)

    def tile_clicked(self, clicked_tile):
        if self.tile_selected is None:  # a tile was not previously selected
            self.tile_selected = clicked_tile
        elif self.tile_selected == clicked_tile:    # cancelling selection
            self.tile_selected = None
        else:   # changing selected tile
            self.tile_selected.click()
            self.tile_selected = clicked_tile
        clicked_tile.click()