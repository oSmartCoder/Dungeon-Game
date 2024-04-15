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
        
        self.win = pygame.display.get_surface()

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
        self.facing_right = True
        self.disable_pursue = False
        self.finished_stun = False
        self.delay = 2
        self.counter = 0
        self.image = self.animations[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Enemy stats
        self.initial_health = self.data['health']
        self.health: int = self.data['health']
        self.damage: int = self.data['damage']
        self.knockback: int = self.data['knockback']

        # Health Bar
        self.health_bar_rect = pygame.Rect(*(self.rect.midtop - Vector2(0, 10)), self.rect.width * 8 / 10, self.rect.height / 6)
        self.health_rect = self.health_bar_rect.copy()

    def import_assets(self):
        assert self.enemy_name in listdir('./assets/enemies/'), 'Enemy not found in assets'

        edited_enemy_name = '_'.join(self.enemy_name.split(' '))

        self.animations = [pygame.transform.scale(image:=pygame.image.load(f'./assets/enemies/{self.enemy_name}/{edited_enemy_name}_{i}.png').convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for i in range(1, 5)]

    def import_enemy_data(self):
        with open('./data/enemy_data.json') as rf:
            self.data: dict = json.load(rf)[self.enemy_name]
        
    def check_collision_with_player(self, player):        
        if pygame.sprite.spritecollide(self, player, False, pygame.sprite.collide_mask):
            print('collided')

    def persue_player(self, player):
        if not self.disable_pursue:
            if Vector2(player.rect.center).distance_to(self.rect.center) <= self.data['pursue radius']:
                self.delta = Vector2(self.rect.center).move_towards(player.rect.center, self.vel) - Vector2(self.rect.center)
            
            else:
                self.delta = Vector2()
    
    def trigger_delay(self):
        if self.disable_pursue:
            if self.counter > self.delay:
                self.counter = 0
                self.triggered_delay = False
                self.disable_pursue = False
                self.image = self.animations[int(self.animation_index)]
            
            else:
                self.counter += 0.1
                self.delta = Vector2()
                self.image = self.mask.to_surface()
                self.image.set_colorkey((0, 0, 0))
     
    def update_image(self):
        image = self.image

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        self.mask = pygame.mask.from_surface(self.image)

    def draw_enemy(self, offset):
        self.win.blit(self.image, self.rect.topleft - offset)

    def update_direction(self, inverse_facing_right=False):
        if self.delta.x > 0:
            self.facing_right = True if not inverse_facing_right else False
            self.direction.x = 1
        elif self.delta.x < 0:
            self.facing_right = False if not inverse_facing_right else True
            self.direction.x = -1
        
        if self.delta.y > 0:
            self.direction.y = 1
        elif self.delta.y < 0:
            self.direction.y = -1

    def update_health_bar(self, offset):
        self.health_bar_rect.midtop = self.rect.midtop - offset - Vector2(0, 10)
        self.health_rect = self.health_bar_rect.copy()
        health_percentage = self.health / self.initial_health
        self.health_rect.width = self.health_bar_rect.width * health_percentage

        if health_percentage >= 0.6:
            colour = COLOURS['green'] 
        elif health_percentage >= 0.3:
            colour = COLOURS['orange']
        else:
            colour = COLOURS['red']

        pygame.draw.rect(self.win, 'black', self.health_bar_rect)        
        pygame.draw.rect(self.win, colour, self.health_rect)
        pygame.draw.rect(self.win, 'white', self.health_bar_rect, 2)
        
    def update(self, player: pygame.sprite.Sprite, offset: Vector2):
        self.persue_player(player)
        self.trigger_delay()
        self.update_direction()
        self.update_image()
        self.update_health_bar(offset)
        self.draw_enemy(offset)