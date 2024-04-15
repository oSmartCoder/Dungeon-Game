import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.mixer import Sound

from random import randint

from settings import *


class CollisionGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    def check_collision(self, active_sprite: Sprite, sprite_group: Group, direction: str, player: Sprite):
        """
        Note: All active sprites must have a delta (rate of change) and rect (sprite rect) attribute
        """

        for sprite in sprite_group:
            if active_sprite in sprite_group:
                collision_condition = active_sprite.rect.colliderect(sprite.rect) and not player in (active_sprite, sprite) and active_sprite != sprite
            else:
                collision_condition = active_sprite.rect.colliderect(sprite.rect)
                
            if collision_condition:
                if direction == 'horizontal':
                    if active_sprite.direction.x > 0:
                        active_sprite.rect.right = sprite.rect.left
                    if active_sprite.direction.x < 0:
                        active_sprite.rect.left = sprite.rect.right
                
                elif direction == 'vertical':
                    if active_sprite.direction.y > 0:
                        active_sprite.rect.bottom = sprite.rect.top

                    elif active_sprite.direction.y < 0:
                        active_sprite.rect.top = sprite.rect.bottom

    def update_active_sprites_position(self, active_sprites: Group, player: Sprite):
        for active_sprite in active_sprites:
            active_sprite.rect.x += active_sprite.delta.x
            self.check_collision(active_sprite, self, 'horizontal', player)
            self.check_collision(active_sprite, active_sprites, 'horizontal', player)

            active_sprite.rect.y += active_sprite.delta.y
            self.check_collision(active_sprite, self, 'vertical', player)
            self.check_collision(active_sprite, active_sprites, 'vertical', player)


class CameraGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2()

        self.shadow_image = pygame.image.load(f'./assets/characters/shadow.png').convert_alpha()

        self.sc_amount = 7

    def center_target_camera(self, target: Sprite):
        self.offset.x = target.rect.centerx - WIN_X / 2
        self.offset.y = target.rect.centery - WIN_Y / 2
    
    def shake_camera(self):
        self.offset.x += randint(-self.sc_amount, self.sc_amount)

    def draw_sprites(self, player: Sprite, active_sprites: Group):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            if sprite in active_sprites:
                self.win.blit(pygame.transform.scale(self.shadow_image, (sprite.rect.width if sprite is player else sprite.rect.width / 1.8, sprite.rect.height / 3.5)), (sprite.rect.bottomleft - self.offset + Vector2(2 if sprite is player else 15, -10)))
            
            else:
                self.win.blit(sprite.image, offset_pos)
    
    def update_enemies(self, player: Sprite, enemy_sprites: Group):
        for sprite in enemy_sprites:
            sprite.update(player, self.offset)
    
    def update_player(self, player: Sprite):
        player.update(self.offset)


class AnimationGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    
    def animate(self):
        for sprite in self.sprites():
            sprite.animation_index += sprite.animation_speed

            if sprite.animation_index >= len(sprite.animations):
                sprite.animation_index = 0

            sprite.image = sprite.animations[int(sprite.animation_index)]


class InteractiveGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    
    def update(self):
        pass


class ActiveGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.enemy_hurt_sound = Sound('./assets/sounds/enemies/enemy_hurt.wav')
        self.enemy_die_sound = Sound('./assets/sounds/enemies/enemy_die.wav')
    
    def check_collision_between_sprites(self, camera_sprites: Group):
        player = self.sprites()[0]
        enemy_sprites = self.sprites()[1:]
        
        for enemy_sprite in enemy_sprites:
            if player.triggered:
                particle_rect_offset = pygame.Rect(*(player.particle_rect.topleft + camera_sprites.offset), *player.particle_rect.size)
                if enemy_sprite.rect.colliderect(particle_rect_offset):
                    if enemy_sprite.health <= 0:
                        enemy_sprite.kill()
                        self.enemy_die_sound.play()

                    elif not enemy_sprite.disable_pursue:
                        enemy_sprite.health -= player.damage
                        self.enemy_hurt_sound.play()                        
                        enemy_sprite.disable_pursue = True

                    else:
                        enemy_sprite.delta = player.origin.move_towards(player.pos, enemy_sprite.knockback) - player.origin
                        enemy_sprite.update_direction(inverse_facing_right=True)
                        camera_sprites.shake_camera()