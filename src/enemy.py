import pygame
from pygame.math import Vector2

import json
from typing import Tuple
from os import listdir

from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[float, float], groups: list, enemy_name: str):
        """
        Note: Parent classes of Enemy (groups) access delta, direction, image, and rect for external calculation and value modification
        """
        super().__init__(groups)
        self.enemy_name = enemy_name

        self.scale_factor = 4

        self.import_assets()
        self.import_enemy_data()

        # Animation setup
        self.animation_index = 0
        self.animation_speed = 0.1

        # Enemy setup
        self.vel = 3
        self.direction = Vector2()
        self.delta = Vector2()
        
        # Enemy properties
        self.disable_pursue = False
        self.triggered_delay = False
        self.delay = 5
        self.counter = 0
        self.facing_right = True
        self.image = self.animations[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=pos)

    def import_assets(self):
        assert self.enemy_name in listdir('./assets/enemies/'), 'Enemy not found in assets'

        edited_enemy_name = '_'.join(self.enemy_name.split(' '))

        self.animations = [pygame.transform.scale(image:=pygame.image.load(f'./assets/enemies/{self.enemy_name}/{edited_enemy_name}_{i}.png').convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for i in range(1, 5)]

    def import_enemy_data(self):
        with open('./src/enemy_stats.json') as rf:
            self.data: dict = json.load(rf)[self.enemy_name]
        
    def check_collision_with_player(self, player):        
        if pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask):
            print('collided')

    def persue_player(self, player):
        self.delta = Vector2(self.rect.center).move_towards(player.rect.center, self.vel) - Vector2(self.rect.center)
    
    def trigger_delay(self):
        if self.triggered_delay:
            if self.counter > self.delay:
                self.triggered_delay = False 
                self.disable_persue = False
                self.counter = 0
            else:
                self.counter += 0.1
                self.delta = Vector2()


    def update_image(self):
        image = self.image

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def update_direction(self):
        if self.delta.x > 0:
            self.facing_right = True 
            self.direction.x = 1
        else:
            self.facing_right = False
            self.direction.x = -1
        
        if self.delta.y > 0:
            self.direction.y = 1
        else:
            self.direction.y = -1

    def update(self, player: pygame.sprite.Sprite):
        if Vector2(player.rect.center).distance_to(self.rect.center) <= self.data['pursue radius'] and not self.disable_pursue:
            self.persue_player(player)
            self.update_direction()
        else:
            self.delta = Vector2()
        
        self.trigger_delay()
        self.update_image()



    
