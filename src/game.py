import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from .player import Player
from .tile import *
from .groups import CollisionGroup, CameraGroup, AnimationGroup, InteractiveGroup
from .enemy import Enemy
from settings import *


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()

        self.collision_sprites = CollisionGroup()

        self.enemy_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.active_sprites = pygame.sprite.Group() # enemy sprites + player sprite

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

        for obj in tmx_data.objects:
            pos = (obj.x / tmx_data.tilewidth * TILE_SIZE, obj.y / tmx_data.tileheight * TILE_SIZE)
            match obj.name:
                case 'Spawn Point':
                    Player(pos, [self.camera_sprites, self.active_sprites, self.player_sprite], self.collision_sprites)

                case _:
                    Enemy(pos, [self.camera_sprites, self.animation_sprites, self.active_sprites, self.enemy_sprites], obj.name)

    def update(self):
        self.win.fill((37, 19, 26))
        
        self.collision_sprites.update_active_sprites_position(self.active_sprites)

        self.animation_sprites.animate()

        self.enemy_sprites.update(self.player_sprite.sprite)

        self.camera_sprites.draw_sprites(self.player_sprite.sprite)
        
        self.camera_sprites.update_player(self.player_sprite.sprite)

        




        


