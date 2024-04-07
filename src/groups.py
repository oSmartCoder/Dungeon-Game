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
            
        self.win.blit(player.animations['shadow'], player.rect.midleft - self.offset + Vector2(3, 20))
        
                        
                    
                        


            



    

        



    






