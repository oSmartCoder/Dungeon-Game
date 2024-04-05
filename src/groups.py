import pygame
from pygame.math import Vector2

from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - WIN_X / 2
        self.offset.y = target.rect.centery - WIN_Y / 2

    
    def custom_draw(self, player: pygame.sprite.Sprite):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.win.blit(sprite.image, offset_pos)


class CollisionGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    
    def collision_update(self, active_sprites: pygame.sprite.Group):
        for active_sprite in active_sprites.sprites():
            for collision_sprite in self.sprites():
                if active_sprite.rect.colliderect(collision_sprite.rect):
                    if active_sprite.direction.x > 0:
                        active_sprite.rect.right = collision_sprite.rect.left
                    elif active_sprite.direction.x < 0:
                        active_sprite.rect.left = collision_sprite.rect.right
                
                    if active_sprite.direction.y > 0:
                        active_sprite.rect.bottom = collision_sprite.rect.top
                    elif active_sprite.direction.y < 0:
                        active_sprite.rect.top = collision_sprite.rect.bottom
                        


            



    

        



    






