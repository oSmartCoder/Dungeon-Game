import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from .player import Player
from .tile import *
from .groups import CameraGroup, AnimationGroup, InteractiveGroup
from settings import *


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()

        
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.camera_sprites = CameraGroup()
        self.interactive_sprites = InteractiveGroup()
        self.animation_sprites = AnimationGroup()

        self.load_level()

    def load_level(self):
        tmx_data = load_pygame('./assets/tmx/level_1.tmx')

        for layer in tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, surface in layer.tiles():
                    pos = (x * TILE_SIZE, y * TILE_SIZE)
                    image = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE))

                    match layer.name:
                        case 'Ground' | 'Bone':
                            Tile(pos, image, self.camera_sprites, layer.name)
                        
                        case 'Wall':
                            Tile(pos, image, [self.camera_sprites, self.collision_sprites], layer.name)
                        
                        case 'Chest' | 'Mini Chest':
                            Chest(pos, image, [self.camera_sprites, self.collision_sprites, self.animation_sprites, self.interactive_sprites], layer.name)

                        case 'Small Red Flask' | 'Large Red Flask' | 'Small Blue Flask' | 'Large Blue Flask':
                            Flask(pos, image, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)

                        case 'Flag':
                            Flag(pos, image, [self.camera_sprites, self.animation_sprites], layer.name)

                        case 'Front Torch' | 'Right Torch' | 'Left Torch' | 'Small Candlestick' | 'Tall Candlestick':
                            Torch(pos, image, [self.camera_sprites, self.animation_sprites], layer.name)

                        case 'Coin':
                            Coin(pos, image, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Ladder':
                            Ladder(pos, image, [self.camera_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Golden Key' | 'Silver Key':
                            Key(pos, image, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Mini Brown Box' | 'Mini Silver Box' | 'Brown Box' | 'Silver Box':
                            Box(pos, image, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
        
                        case 'Door':
                            Door(pos, image, [self.camera_sprites, self.interactive_sprites], layer.name)

                        case _:
                            raise ValueError(f'Cannot assign layer \'{layer.name}\' to associated class')

        spawn_point_pos = (obj:=tmx_data.get_object_by_name('Spawn Point')).x / tmx_data.tilewidth * TILE_SIZE, obj.y / tmx_data.tileheight * TILE_SIZE

        Player(spawn_point_pos, [self.camera_sprites, self.active_sprites], self.collision_sprites)
        

    def update(self):
        self.win.fill((37, 19, 26))

        self.animation_sprites.animate()
    
        self.camera_sprites.custom_update(self.active_sprites.sprites()[0])

        


