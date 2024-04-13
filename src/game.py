import pygame
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from .player import Player
from .tile import *
from .groups import CollisionGroup, CameraGroup, AnimationGroup, InteractiveGroup
from .enemy import Enemy
from .health_bar import HealthBar
from settings import *


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()

        self.collision_sprites = CollisionGroup()

        self.enemy_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.active_sprites = pygame.sprite.Group() # enemy sprites + player sprite

        self.camera_sprites = CameraGroup()
        self.interactive_sprites = InteractiveGroup()
        self.animation_sprites = AnimationGroup()

        self.load_level()

        self.health_bar = HealthBar((20, 20), 100)


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
                    Player(pos, [self.camera_sprites, self.active_sprites, self.player])

                case _:
                    Enemy(pos, [self.camera_sprites, self.animation_sprites, self.active_sprites, self.enemy_sprites], obj.name)

    def check_collision_between_active_sprites(self):
        for enemy_sprite in self.enemy_sprites:
            if self.player.sprite.triggered:
                particle_rect_offset = pygame.Rect(*(self.player.sprite.particle_rect.topleft + self.camera_sprites.offset), *self.player.sprite.particle_rect.size)
                if enemy_sprite.rect.colliderect(particle_rect_offset):
                    enemy_sprite.disable_persue = True
                    enemy_sprite.delta = self.player.sprite.origin.move_towards(self.player.sprite.pos, enemy_sprite.data['knockback']) - self.player.sprite.origin

                    enemy_sprite.update_direction()
                    self.camera_sprites.shake_camera()
                
                else:
                    enemy_sprite.triggered_delay = True

    def update(self):
        self.win.fill((37, 19, 26))
        
        self.collision_sprites.update_active_sprites_position(self.active_sprites, self.player.sprite)

        self.enemy_sprites.update(self.player.sprite)

        self.camera_sprites.center_target_camera(self.player.sprite)
        self.check_collision_between_active_sprites()
        self.camera_sprites.draw_sprites(self.player.sprite, self.active_sprites)
        self.camera_sprites.update_player(self.player.sprite)

        self.animation_sprites.animate()

        self.health_bar.update()

        




        


