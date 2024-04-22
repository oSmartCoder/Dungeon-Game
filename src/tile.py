import pygame

from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], surface: pygame.Surface, groups: list[pygame.sprite.Group], layer_name: str) -> None:
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.layer_name = layer_name


class Chest(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Chest':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/chest/chest_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case 'Mini Chest':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/mini_chest/mini_chest_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
        
        super().__init__(pos, self.animations[0], groups, layer_name)

        self.animation_index = 0
        self.animation_speed = 0.1
                

class Coin(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Coin':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/coin/coin_{i}.png'), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
            
        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1
            

class Flask(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Small Blue Flask':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/flasks/small_blue_flask_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case 'Small Red Flask':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/flasks/small_red_flask_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Large Blue Flask':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/flasks/large_blue_flask_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case 'Large Red Flask':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/flasks/large_red_flask_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
            
        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1


class Key(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Golden Key':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/keys/golden_key_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case 'Silver Key':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/keys/silver_key_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')

        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1


class Torch(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Front Torch':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/torch/front_torch_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]
            
            case 'Left Torch':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/torch/side_torch_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Right Torch':
                self.animations = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/torch/side_torch_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)), True, False) for i in range(1, 5)]

            case 'Small Candlestick':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/torch/small_candlestick_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Tall Candlestick':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/torch/tall_candlestick_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
            
        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1


class Flag(Tile):
    def __init__(self, pos, groups, layer_name):
        match layer_name:
            case 'Flag':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/flag/flag_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
            
        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1


class Box(Tile):
    def __init__(self, pos, groups, layer_name):    
        match layer_name:
            case 'Mini Silver Box':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/mini_silver_box/mini_silver_box_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Mini Brown Box':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/mini_brown_box/mini_brown_box_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Silver Box':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/silver_box/silver_box_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case 'Brown Box':
                self.animations = [pygame.transform.scale(pygame.image.load(f'./assets/sprite animations/brown_box/brown_box_{i}.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)) for i in range(1, 5)]

            case _:
                raise ValueError(f'Cannot assign layer \'{layer_name}\' to {__class__.__name__}.animations')
            
        super().__init__(pos, self.animations[0], groups, layer_name)
    
        self.animation_index = 0
        self.animation_speed = 0.1