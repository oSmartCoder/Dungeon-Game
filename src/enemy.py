import pygame
from pygame.math import Vector2
from pygame.mixer import Sound

import json
from typing import Tuple
from os import listdir
from math import sqrt

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

        self.import_images()
        self.import_sounds()
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
        self.stunned_delay = 2
        self.stunned_counter = 0

        self.triggered = False
        self.attack_state = False
        self.last_player_coords = Vector2()
        self.last_enemy_coords = Vector2()
        self.new_coords = Vector2()
        self.attack_cooldown_counter = self.data['attack cooldown']
        self.total_attack_delta = Vector2()


        self.image = self.animations[int(self.animation_index)]
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

        # Enemy stats
        self.initial_health = self.data['health']
        self.health: int = self.data['health']
        self.damage: int = self.data['damage']
        self.knockback: int = self.data['knockback']
        self.attack_cooldown = self.data['attack cooldown']
        self.leap_speed = self.data['leap speed']
        self.coin_drops = self.data['coin drops']

        # Health Bar
        self.health_bar_rect = pygame.Rect(*(self.rect.midtop - Vector2(0, 10)), self.rect.width * 8 / 10, self.rect.height / 6)
        self.health_rect = self.health_bar_rect.copy()

        # Font
        self.font = pygame.font.Font('./assets/fonts/font.ttf', 30)

    def import_images(self):
        assert self.enemy_name in listdir('./assets/enemies/'), 'Enemy not found in assets'

        edited_enemy_name = '_'.join(self.enemy_name.split(' '))

        self.animations = [pygame.transform.scale_by(pygame.image.load(f'./assets/enemies/{self.enemy_name}/{edited_enemy_name}_{i}.png').convert_alpha(), self.scale_factor) for i in range(1, 5)]

    def import_sounds(self):
        self.enemy_leap_sound = Sound('./assets/sounds/enemies/enemy_leap.mp3')

    def import_enemy_data(self):
        with open('./data/enemy_data.json') as rf:
            self.data: dict = json.load(rf)[self.enemy_name]
        
    def persue_player(self, player):
        if self.disable_pursue or self.triggered:
            return

        distance = Vector2(player.rect.center).distance_to(self.rect.center)

        if distance <= self.data['attack radius']:
            self.attack_state = True
            self.last_player_coords = Vector2(player.rect.center)
            self.last_enemy_coords = Vector2(self.rect.center)

        elif distance <= self.data['pursue radius']:
            self.delta = Vector2(self.rect.center).move_towards(player.rect.center, self.vel) - Vector2(self.rect.center)
        
        else:
            self.delta = Vector2()
    
    def trigger_delay(self):
        if self.disable_pursue:
            if self.stunned_counter > self.stunned_delay:
                self.stunned_counter = 0
                self.disable_pursue = False
                self.image = self.animations[int(self.animation_index)]
            else:
                self.stunned_counter += 0.1
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
        
    def get_new_vector(self, x1: float, y1: float, x2: float, y2: float, d: float) -> tuple[float, float]:
        if x2 - x1 == 0:
            x3 = float(x1)
            
            if y2 - y1 > 0: # if player is below the enemy
                y3 = y1 + d

            elif y2 - y1 < 0: # if player is above the enemy
                y3 = y1 - d

            else:
                raise ValueError('y2 - y1 should not be zero.')
        
        elif y2 - y1 == 0:
            y3 = float(y1)

            if x2 - x1 > 0: # if player is to the right of enemy
                x3 = x1 + d

            elif x2 - x1 < 0: # if player is to the left of enemy
                x3 = x1 - d
            
            else:
                raise ValueError('x2 - x1 should not be zero.')

        else:
            m = (y2 - y1) / (x2 - x1)
            c = y1 - (m * x1)

            f = lambda x: m * x + c

            x3 = (-sqrt(2*c*(y1- x1*m) - (y1 - x1*m)**2 - c**2 + d**2*(m**2 + 1) + x1 - c*m + y1*m)) / m**2 + 1

            y3 = f(x3)
        
        return Vector2(x3, y3)
    
    def attack_player(self, player):
        if not self.attack_state:
            return
        
        if self.attack_cooldown_counter >= self.attack_cooldown:
            self.triggered = True
            # self.enemy_leap_sound.play()
        else:
            self.attack_cooldown_counter += 0.1

        if self.triggered:
            if self.total_attack_delta.distance_to(Vector2(0, 0)) >= self.data['leap distance']:
                self.attack_state = False
                self.triggered = False
                self.total_attack_delta = Vector2()
                self.attack_cooldown_counter = 0

            else:
                # Calculates new point given the origin point, rule, and distance to that point
                d = self.data['leap distance']
                x1, y1 = self.last_enemy_coords
                x2, y2 = self.last_player_coords
                x3, y3 = self.get_new_vector(x1, y1, x2, y2, d)

                self.delta = Vector2(x1, y1).move_towards((x3, y3), self.leap_speed) - Vector2(x1, y1)
                self.player_delta = Vector2(x1, y1).move_towards((x3, y3), player.knockback) - Vector2(x1, y1)

                # since pygame flips the y axis, we have to calculate for new delta values
                if x2 - x1 > 0:
                    self.delta *= -1
                    self.player_delta *= -1

                self.total_attack_delta += self.delta
    
    def update(self, player: pygame.sprite.Sprite, offset: Vector2):
        self.persue_player(player)
        self.attack_player(player)
        self.trigger_delay()
        self.update_direction()
        self.update_image()
        self.update_health_bar(offset)
        self.draw_enemy(offset)