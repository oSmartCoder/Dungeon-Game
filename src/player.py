import pygame
from pygame.math import Vector2



class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups, collision_sprites):
        super().__init__(groups)

        self.win = pygame.display.get_surface()

        # Sprite group setup
        self.collision_sprites = collision_sprites
        self.camera_group = groups[0]

        # General setup
        self.scale_factor = 4
        self.weapon_scale_factor = 3
        self.animation_index = 0
        self.animation_speed = 0.15
        self.vel = 5
        self.controls = {
            'a': pygame.K_a,
            'd': pygame.K_d,
            's': pygame.K_s,
            'w': pygame.K_w
        }
    
        # Load assets
        self.import_assets()

        # Player setup
        self.direction = Vector2()
        self.facing_right = True
        self.facing_up = False
        self.status = 'idle'
        self.image = self.animations[self.status][self.animation_index]
        self.rect = self.image.get_rect(center=pos)

    
        # Weapon setup
        self.weapon_rect = self.weapon.get_rect()

    def import_assets(self):
        self.animations = {
            'idle': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/idle{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * (self.scale_factor + 0.2))) for i in range(1, 3)],
            'run': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/run{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * (self.scale_factor + 0.2))) for i in range(1, 5)],
            'idle-up': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/idle-up{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * (self.scale_factor + 0.2))) for i in range(1, 4)],
            'run-up': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/run-up{i}.png')).convert_alpha(), (image.get_width() * self.scale_factor, image.get_height() * (self.scale_factor + 0.2))) for i in range(1, 4)],
            'shadow': pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/shadow.png').convert_alpha()), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor))
        }
        
        self.weapon = pygame.transform.scale((image:=pygame.image.load('./assets/weapons/wooden/wooden_sword.png')), (image.get_width() * self.weapon_scale_factor, image.get_height() * self.weapon_scale_factor)).convert_alpha()

    def animate(self):
        self.animation_index += self.animation_speed * 0.1 if self.status == 'idle' and int(self.animation_index) == 0 else self.animation_speed
        
        if self.animation_index >= len(self.animations[self.status]):
            self.animation_index = 0
        
        image = self.animations[self.status][int(self.animation_index)]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def movement(self):
        keys = pygame.key.get_pressed()

        if not any([keys[control] for control in self.controls.values()]):
            self.status = 'idle' if not self.facing_up else 'idle-up'
        
        if keys[self.controls['d']]:
            self.facing_right = True
            self.status = 'run'
            self.direction.x = 1
        elif keys[self.controls['a']]:
            self.facing_right = False
            self.status = 'run' 
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[self.controls['s']]:
            self.status = 'run'
            self.facing_up = False
            self.direction.y = 1
        elif keys[self.controls['w']]:
            self.status = 'run-up'
            self.facing_up = True
            self.direction.y = -1
        else:
            self.direction.y = 0

        # Normalise vector movement (so that diagonal movement won't go 41% faster)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * self.vel
        self.check_collision('horizontal')
        self.rect.y += self.direction.y * self.vel
        self.check_collision('vertical')              

    def draw_shadow(self, offset):
        self.win.blit(self.animations['shadow'], self.rect.midleft - offset + Vector2(3, 20))

    def draw_player(self, offset):
        self.win.blit(self.image, self.rect.topleft - offset)

    def check_collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left

                    if self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top

                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def sword_mechanics(self):
        pos = pygame.mouse.get_pos()

        self.win.blit(self.weapon, pos - Vector2(self.weapon_rect.centerx, self.weapon_rect.centery))


    def update(self, offset):
        self.draw_shadow(offset)
        self.draw_player(offset)
        self.movement()        
        self.animate()
        self.sword_mechanics()