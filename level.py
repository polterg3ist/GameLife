import pygame
from settings import *
from field import Field
from random import randint


class Level:
    def __init__(self):
        # game setup
        self.game_run = False
        # game field and field camera
        self.field = Field()
        self.field.create_field()
        self.field.centralize_camera()

    def randomize_field(self):
        for cell in self.field.sprites():
            if not randint(0, 10):
                cell.active = True
            else:
                cell.active = False

    def mouse_click(self, mousebutton):
        # this function getting the column and row of clicked cell
        offset = self.field.offset

        # getting mouse position
        mx, my = pygame.mouse.get_pos()  # mx - mouseX | my - mouseY
        mx -= offset.x
        my -= offset.y

        col = int(mx / self.field.cell_width)
        row = int(my / self.field.cell_height)

        self.cell_click(col, row, mousebutton)

    def cell_click(self, col, row, mousebutton):
        if CELLS_AMOUNT_X > col >= 0 and CELLS_AMOUNT_Y > row >= 0:
            cell = self.field.cells_field[row][col]
            if mousebutton == 'left':
                cell.active = True
            elif mousebutton == 'right':
                cell.active = False

    def start_or_pause_game(self):
        self.game_run = not self.game_run

    def clear_field(self):
        for cell in self.field.sprites():
            cell.active = False

    def run(self):
        self.field.custom_draw()
        self.field.get_camera_input()

        if self.game_run:
            self.field.game_logic()
            self.field.check_turn_cooldown()
