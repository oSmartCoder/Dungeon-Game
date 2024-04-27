import pygame
from pygame.mixer import Sound
from pytmx import TiledTileLayer
from pytmx.util_pygame import load_pygame

from random import randint as rand

from .player import Player
from .tile import *
from .groups import CollisionGroup, CameraGroup, AnimationGroup, InteractiveGroup, ActiveGroup
from .enemy import Enemy
from settings import *
from support import display_text
from decorators import run_once


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()

        self.collision_sprites = CollisionGroup()

        self.enemy_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.active_sprites = ActiveGroup() # enemy sprites + player sprite

        self.camera_sprites = CameraGroup()
        self.interactive_sprites = InteractiveGroup()
        self.animation_sprites = AnimationGroup()

        self.load_level()

        self.coin_image = pygame.transform.scale(pygame.image.load('./assets/sprite animations/coin/coin_1.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))

        self.game_over = False
        self.victory = False

    @run_once
    def play_music(self):
        self.music = Sound(f'./assets/sounds/music/otherworld.mp3')
        self.music.set_volume(0.8)
        self.music.play(loops=-1, fade_ms=5000)

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
                            Chest(pos, [self.camera_sprites, self.collision_sprites, self.animation_sprites, self.interactive_sprites], layer.name)

                        case 'Small Red Flask' | 'Large Red Flask' | 'Small Blue Flask' | 'Large Blue Flask':
                            Flask(pos, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)

                        case 'Flag':
                            Flag(pos, [self.camera_sprites, self.animation_sprites], layer.name)

                        case 'Front Torch' | 'Right Torch' | 'Left Torch' | 'Small Candlestick' | 'Tall Candlestick':
                            Torch(pos, [self.camera_sprites, self.animation_sprites], layer.name)

                        case 'Coin':
                            Coin(pos, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Ladder':
                            Tile(pos, image, [self.camera_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Golden Key' | 'Silver Key':
                            Key(pos, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
                        
                        case 'Mini Brown Box' | 'Mini Silver Box' | 'Brown Box' | 'Silver Box':
                            Box(pos, [self.camera_sprites, self.animation_sprites, self.interactive_sprites], layer.name)
        
                        case 'Door':
                            Tile(pos, image, [self.camera_sprites, self.interactive_sprites], layer.name)

                        case _:
                            raise ValueError(f'Cannot assign layer \'{layer.name}\' to associated class')

        for obj in tmx_data.objects:
            pos = (obj.x / tmx_data.tilewidth * TILE_SIZE, obj.y / tmx_data.tileheight * TILE_SIZE)
            match obj.name:
                case 'Spawn Point':
                    Player(pos, [self.camera_sprites, self.active_sprites, self.player])

                case _:
                    Enemy(pos, [self.camera_sprites, self.animation_sprites, self.active_sprites, self.enemy_sprites], obj.name)
                
    def display_coin_counter(self):
        self.win.blit(self.coin_image, (10, 70))

        display_text(self.win, f'x{self.player.sprite.coins}', (66, 91), position='topleft')

    def update(self):        
        self.collision_sprites.update_active_sprites_position(self.active_sprites, self.player.sprite)

        self.camera_sprites.draw_sprites(self.player.sprite, self.active_sprites)
        
        self.camera_sprites.update_enemies(self.player.sprite, self.enemy_sprites)

        self.camera_sprites.center_target_camera(self.player.sprite)

        self.game_over = self.active_sprites.check_collision_between_sprites(self.camera_sprites, self.animation_sprites, self.interactive_sprites)
        
        if self.game_over:
            self.music.stop()
        
        self.camera_sprites.update_player(self.player.sprite)

        self.animation_sprites.animate()

        self.victory = self.interactive_sprites.update_collision(self.player.sprite)

        if self.victory:
            self.music.stop()

        self.interactive_sprites.update_sprites(self.player.sprite)

        self.display_coin_counter()

