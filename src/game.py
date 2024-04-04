import pygame
from pytmx.util_pygame import load_pygame

from .player import Player
from .tile import Tile
from settings import *

class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()


        self.visible_sprites = pygame.sprite.Group()

        Player((400, 400), self.visible_sprites)


        self.load_level()

    def load_level(self):
        
        tmx_data = load_pygame('./assets/tmx/level_1.tmx')

        # print(tmx_data.width, tmx_data.tilewidth, tmx_data.height, tmx_data.tileheight)


        for layer in tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_SIZE, y * TILE_SIZE)

                    image = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE))
                    Tile(pos, image, self.visible_sprites)
                


        


    def update(self):
        self.win.fill((37, 19, 26))

        self.visible_sprites.draw(self.win)
        self.visible_sprites.update()


