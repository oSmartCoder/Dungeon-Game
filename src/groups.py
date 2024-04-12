import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite, Group

from settings import *


class CollisionGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()
    
    def check_collision(self, active_sprite: Sprite, direction: str):
        """
        Note: All active sprites must have a delta (rate of change) and rect (sprite rect) attribute
        """
        for collision_sprite in self.sprites():
            if active_sprite.rect.colliderect(collision_sprite.rect):
                if direction == 'horizontal':
                    if active_sprite.direction.x > 0:
                        active_sprite.rect.right = collision_sprite.rect.left
                    if active_sprite.direction.x < 0:
                        active_sprite.rect.left = collision_sprite.rect.right
                
                elif direction == 'vertical':
                    if active_sprite.direction.y > 0:
                        active_sprite.rect.bottom = collision_sprite.rect.top

                    elif active_sprite.direction.y < 0:
                        active_sprite.rect.top = collision_sprite.rect.bottom

    def update_active_sprites_position(self, active_sprites: Group):
        for active_sprite in active_sprites.sprites():
            active_sprite.rect.x += active_sprite.delta.x
            self.check_collision(active_sprite, 'horizontal')

            active_sprite.rect.y += active_sprite.delta.y
            self.check_collision(active_sprite, 'vertical')



class CameraGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2()

    def center_target_camera(self, target: Sprite):
        self.offset.x = target.rect.centerx - WIN_X / 2
        self.offset.y = target.rect.centery - WIN_Y / 2
    
    def draw_sprites(self, player: Sprite):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            
            if sprite != player:
                self.win.blit(sprite.image, offset_pos)
    
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





            
        
        
                        
                    
                        


            



    

        



    






