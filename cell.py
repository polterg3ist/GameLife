import pygame


class Cell(pygame.sprite.Sprite):
    def __init__(self, groups, posx, posy, width, height):
        super().__init__(groups)
        self.rect = pygame.Rect(posx, posy, width, height)
        self.active = False
