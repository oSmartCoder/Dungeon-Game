import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from .player import Player
from .tile import Tile
from .groups import CameraGroup

from settings import *


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()


        self.camera_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.moveable_sprites = pygame.sprite.Group()

        self.load_level()

    def load_level(self):
        
        tmx_data = load_pygame('./assets/tmx/level_1.tmx')


        print(dir(tmx_data))

        print(tmx_data)

        for i, layer in enumerate(tmx_data.visible_layers):

            
            if isinstance(layer, TiledTileLayer):
                for x, y, surface in layer.tiles():

                    
                    
                    pos = (x * TILE_SIZE, y * TILE_SIZE)
                    image = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE))

                    # Priority Order
                    match layer.name:
                        case 'Ground' | 'Bones' | 'Torches' | 'Flags':
                            Tile(pos, image, self.camera_sprites, layer.name)
                        
                        case 'Walls' | 'Chest':
                            Tile(pos, image, [self.camera_sprites, self.collision_sprites], layer.name)

                        case 'Doors':
                            Tile(pos, image, [self.camera_sprites, self.moveable_sprites], layer.name)
          

        pos = (obj:=tmx_data.get_object_by_name('Spawn Point')).x / tmx_data.tilewidth * TILE_SIZE, obj.y / tmx_data.tileheight * TILE_SIZE

        Player(pos, [self.camera_sprites, self.active_sprites], self.collision_sprites)
        

    def update(self):
        self.win.fill((37, 19, 26))

        
    
        self.camera_sprites.custom_draw(self.active_sprites.sprites()[0])
        
        self.camera_sprites.update()

        


