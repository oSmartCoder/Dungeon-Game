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

    
    def custom_update(self, player: pygame.sprite.Sprite):
        self.center_target_camera(player)

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            
            if sprite != player:
                self.win.blit(sprite.image, offset_pos)
        
        player.update(self.offset)


class AnimationGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    
    def animate(self):
        for sprite in self.sprites():

            sprite.animation_index += sprite.animation_speed

            if sprite.animation_index >= len(sprite.animations):
                sprite.animation_index = 0

            sprite.image = sprite.animations[int(sprite.animation_index)]



class InteractiveGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    
    def update(self):
        pass

            
        
        
                        
                    
                        


            



    

        



    






