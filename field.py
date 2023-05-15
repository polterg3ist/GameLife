import pygame
from settings import *
from cell import Cell


class Field(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        # general setup
        self.offset = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.cells_field = []
        self.camera_direction = pygame.math.Vector2()

        # cell size
        self.cell_width = 16
        self.cell_height = 16

        # camera
        self.camera_speed = 15

        # game refresh
        self.turn_cooldown = 500    # 500 milliseconds
        self.turn_time = None
        self.can_turn = True

    def create_field(self):
        for row in range(CELLS_AMOUNT_Y):
            line = []
            for index in range(CELLS_AMOUNT_X):
                x = index * self.cell_width
                y = row * self.cell_height
                cell = Cell([self], x, y, self.cell_width, self.cell_height)
                line.append(cell)
            self.cells_field.append(line)

    def get_camera_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.camera_direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.camera_direction.y = -1
        else:
            self.camera_direction.y = 0

        if keys[pygame.K_LEFT]:
            self.camera_direction.x = 1
        elif keys[pygame.K_RIGHT]:
            self.camera_direction.x = -1
        else:
            self.camera_direction.x = 0

    def check_turn_cooldown(self):
        if not self.can_turn:
            current_time = pygame.time.get_ticks()
            if current_time - self.turn_time >= self.turn_cooldown:
                self.can_turn = True

    def game_logic(self):
        # break the function if cant make a turn
        if not self.can_turn:
            return

        changes = []  # list for all cells that need to be inverted
        self.turn_time = pygame.time.get_ticks()
        self.can_turn = False

        for row, line in enumerate(self.cells_field):
            for col, cell in enumerate(line):
                if row == 0:
                    if col == 0:
                        neighbors = [self.cells_field[row][col+1], self.cells_field[row+1][col+1],
                                     self.cells_field[row+1][col]]

                    elif col == CELLS_AMOUNT_X - 1:
                        neighbors = [self.cells_field[row][col-1], self.cells_field[row+1][col],
                                     self.cells_field[row+1][col-1]]

                    else:
                        neighbors = [self.cells_field[row][col+1], self.cells_field[row+1][col+1],
                                     self.cells_field[row+1][col], self.cells_field[row+1][col-1],
                                     self.cells_field[row][col-1]]

                elif row == CELLS_AMOUNT_Y - 1:
                    if col == 0:
                        neighbors = [self.cells_field[row][col + 1], self.cells_field[row - 1][col + 1],
                                     self.cells_field[row - 1][col]]

                    elif col == CELLS_AMOUNT_X - 1:
                        neighbors = [self.cells_field[row][col - 1], self.cells_field[row - 1][col],
                                     self.cells_field[row - 1][col - 1]]

                    else:
                        neighbors = [self.cells_field[row][col + 1], self.cells_field[row - 1][col + 1],
                                     self.cells_field[row - 1][col], self.cells_field[row - 1][col - 1],
                                     self.cells_field[row][col - 1]]
                else:
                    if col == 0:
                        neighbors = [self.cells_field[row][col + 1], self.cells_field[row - 1][col + 1],
                                     self.cells_field[row - 1][col], self.cells_field[row + 1][col + 1],
                                     self.cells_field[row + 1][col]]

                    elif col == CELLS_AMOUNT_X - 1:
                        neighbors = [self.cells_field[row][col - 1], self.cells_field[row - 1][col - 1],
                                     self.cells_field[row - 1][col], self.cells_field[row + 1][col - 1],
                                     self.cells_field[row + 1][col]]

                    else:
                        neighbors = [self.cells_field[row][col + 1], self.cells_field[row - 1][col + 1],
                                     self.cells_field[row - 1][col], self.cells_field[row - 1][col - 1],
                                     self.cells_field[row][col - 1], self.cells_field[row + 1][col - 1],
                                     self.cells_field[row+1][col], self.cells_field[row+1][col+1]]

                active_neighbors_count = len(list(filter(lambda x: x.active, neighbors)))

                if not cell.active:
                    if active_neighbors_count == BORN:
                        changes.append(cell)
                else:
                    if active_neighbors_count not in SURVIVE:
                        changes.append(cell)

        # applying changes
        self.make_changes(changes)

    def make_changes(self, changes):
        for cell in changes:
            cell.active = not cell.active

    def change_cells_size(self, x, y):
        if x < 0 and self.cell_width >= 8 or x > 0 and self.cell_width <= 200:
            shift = pygame.math.Vector2()
            for row_index, row in enumerate(self.cells_field):
                shift.y = row_index * y
                for col_index, col in enumerate(row):
                    shift.x = col_index * x
                    col.rect.inflate_ip(x, y)
                    col.rect.topleft += shift

            self.cell_width += x
            self.cell_height += y

    def centralize_camera(self):
        centerx = (self.cell_width * CELLS_AMOUNT_X) // 4
        centery = (self.cell_height * CELLS_AMOUNT_Y) // 4
        shift = pygame.math.Vector2(centerx, centery)
        self.offset.xy = (-centerx, -centery)

        for index_row, row in enumerate(self.cells_field):
            # self.cell_height can be also self.cell_width because cell is square by default
            #shift.y -= index_row * self.cell_height
            for index_cell, cell in enumerate(row):
                #shift.x -= index_cell * self.cell_width
                cell.rect.topleft -= shift

    def custom_draw(self):
        self.offset.x += self.camera_direction.x * self.camera_speed
        self.offset.y += self.camera_direction.y * self.camera_speed

        for sprite in self.sprites():
            sprite.rect.x += self.camera_direction.x * self.camera_speed
            sprite.rect.y += self.camera_direction.y * self.camera_speed

            if sprite.active:
                # cell filled black
                pygame.draw.rect(self.display_surface, "black", sprite.rect)
            else:
                # cell with black outline
                pygame.draw.rect(self.display_surface, "gray", sprite.rect, 1)
