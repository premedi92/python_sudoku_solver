import pygame as pygame
import colors as colors
import numpy as numpy
import copy as copy


class Button:
    def __init__(self, color, rect, string, font, click_function):
        self.color = color
        self.rect = rect
        self.string = string
        self.font = font
        self.is_pressed = False
        self.click_function = click_function

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, colors.BLACK, self.rect, 1)  # draws a border
        w, h = self.font.size(self.string)
        text = self.font.render(self.string, True, colors.BLACK, self.color)
        win.blit(text, numpy.subtract(self.rect.center, (w // 2, h // 2)))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def copy(self):
        return Button(self.color, self.rect.copy(), self.string, self.font, self.click_function)

    def click(self):
        self.click_function()

    def set_string(self, string):
        self.string = string

    def set_click_function(self, func):
        self.click_function = func


class ButtonCluster:
    def __init__(self, rect, color, visible, arrangement):
        self.rect = rect
        self.color = color
        self.visible = visible
        self.arrangement = arrangement
        self.button_list = []

    def add_button(self, button):
        self.button_list.append(button)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

        total_button_height = 0

        for button in self.button_list:
            total_button_height += button.rect.height

        y_sep = (self.rect.height - total_button_height) // (len(self.button_list) + 1)
        y_zero = self.rect.y

        for button in self.button_list:
            x_sep = (self.rect.width - button.rect.width) // 2
            button.rect.x = self.rect.x + x_sep
            button.rect.y = y_zero + y_sep
            y_zero = button.rect.y + button.rect.height
            button.draw(win)