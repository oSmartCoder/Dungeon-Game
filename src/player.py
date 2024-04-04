import pygame
from math import sqrt

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, *groups):
        super().__init__(*groups)

        self.win = pygame.display.get_surface()


        self.scale_factor = 4
        self.animation_index = 0
        self.animation_speed = 0.1
        self.vel = 5

        self.animations = {
            'idle': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/idle{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for i in range(4)],
            'run': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/run{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for i in range(4)]
        }



        self.facing_right = True
        self.status = 'idle'

        self.image = self.animations[self.status][self.animation_index]

        self.rect = self.image.get_rect(topleft=pos)

        self.controls = {
            'a': pygame.K_a,
            'd': pygame.K_d,
            's': pygame.K_s,
            'w': pygame.K_w
        }
        

    def animate(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= len(self.animations[self.status]):
            self.animation_index = 0


        image = self.animations[self.status][int(self.animation_index)]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

 
    def movement(self):
        keys = pygame.key.get_pressed()

        self.status = 'run' if any([keys[control] for control in self.controls.values()]) else 'idle'

        dx, dy = 0, 0

        if keys[self.controls['a']]:
            self.facing_right = False        
            dx -= self.vel
        
        if keys[self.controls['d']]:
            self.facing_right = True

            dx += self.vel

        if keys[self.controls['w']]:
            dy -= self.vel
        
        if keys[self.controls['s']]:
            dy += self.vel

        # Normalise vector movement (so that diagonal movement won't go 41% faster)
        if any([keys[vertical] for vertical in (self.controls['w'], self.controls['s'])]) and any([keys[horizontal] for horizontal in (self.controls['a'], self.controls['d'])]):
            dx /= sqrt(2)
            dy /= sqrt(2)

        self.rect.x += dx
        self.rect.y += dy


    def draw(self):
        self.win.blit(self.image, self.rect)

    def update(self):
        self.draw()
        self.movement()
        self.animate()