import pygame
from settings import *
from level import Level


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[0]:
                self.level.mouse_click(mousebutton='left')
            elif mouse_keys[2]:
                self.level.mouse_click(mousebutton='right')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:

                    # pause/unpause game
                    if event.key == pygame.K_SPACE:
                        self.level.start_or_pause_game()
                    # randomize cells on field
                    elif event.key == pygame.K_r:
                        self.level.randomize_field()

                    # control game speed
                    elif event.key == pygame.K_EQUALS:
                        self.level.field.turn_cooldown += 100
                    elif event.key == pygame.K_MINUS and self.level.field.turn_cooldown > 0:
                        self.level.field.turn_cooldown -= 100

                    # clear game field
                    elif event.key == pygame.K_c:
                        self.level.clear_field()

                # control size of cells
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        self.level.field.change_cells_size(-1, -1)
                    elif event.y > 0:
                        self.level.field.change_cells_size(1, 1)

            pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}  |  DELAY: "
                                       f"{self.level.field.turn_cooldown}")

            self.screen.fill(BACKGROUND_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
