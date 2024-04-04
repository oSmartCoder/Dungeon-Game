import pygame
from pytmx.util_pygame import load_pygame

from .player import Player
from settings import *

class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()


        self.visible_sprites = pygame.sprite.Group()

        Player((400, 400), self.visible_sprites)



    def background(self):
        self.win.fill((0, 0, 0))

    def update(self):
        self.background()
        self.visible_sprites.update()

