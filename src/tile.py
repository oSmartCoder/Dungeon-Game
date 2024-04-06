import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, layer_name):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.layer_name = layer_name


class AnimatedTile(Tile):
    def __init__(self, pos, surface, groups, layer_name):
        super().__init__(pos, surface, groups, layer_name)
        

