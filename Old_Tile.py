import pygame as pygame
import colors as colors
import Button as Button


class Tile:
    def __init__(self, num, row, col, width):
        self.num = num
        self.row = row
        self.col = col
        self.width = width
        self.x = col * width
        self.y = row * width
        self.fixed = False

    def set_to(self, num):
        if not self.fixed:
            self.num = num

    def clear(self):
        if not self.fixed:
            self.num = None

    def unfix(self):
        self.fixed = False

    def fix(self):
        self.fixed = True

    def is_last(self):
        return self.row == 8 and self.col == 8

    def draw(self, win, fast=True):
        if not fast:
            pygame.draw.rect(win, colors.SUD_YELLOW, (self.x, self.y, self.width, self.width))
            pygame.draw.rect(win, colors.BLACK, (self.x, self.y, self.width, self.width), 1)

        if self.num:
            if self.fixed:
                num_color = colors.RED
            else:
                num_color = colors.BLACK
            font = pygame.font.SysFont("Arial", self.width // 1)
            w, h = font.size(str(self.num))
            num = font.render(str(self.num), True, num_color, colors.SUD_YELLOW)
            win.blit(num, (self.x + self.width // 2 - w // 2, self.y + self.width // 2 - h // 2))
            # win.blit(num, (self.x, self.y))
