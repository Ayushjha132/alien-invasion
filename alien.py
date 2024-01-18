import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        super().__init__()

        self.screen = ai_game.screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        """adding the space to left and from the top of alien img both equal to width and height of alien"""
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        """alien move in horizontally"""
        self.x = float(self.rect.x)

