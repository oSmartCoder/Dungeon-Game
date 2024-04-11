import pygame
from pygame.math import Vector2

from math import degrees, atan2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups, collision_sprites):
        super().__init__(groups)

        self.win = pygame.display.get_surface()

        # Sprite group setup
        self.collision_sprites = collision_sprites
        self.camera_group = groups[0]

        # Player setup
        self.p_scale_factor = 4
        self.p_animation_index = 0
        self.p_animation_speed = 0.15

        # Weapon setup
        self.w_scale_factor = 4
        self.w_counter = 0
        self.w_delay = 1
        self.triggered = False
        self.sword_direction = 1
        self.origin, self.pos = Vector2(), Vector2()
        self.clicked = False

        # Player controls
        self.vel = 5
        self.controls = {
            'a': pygame.K_a,
            'd': pygame.K_d,
            's': pygame.K_s,
            'w': pygame.K_w
        }

        # Load assets
        self.import_assets()

        # Player properties
        self.direction = Vector2()
        self.facing_right = True
        self.facing_up = False
        self.status = 'idle'
        self.image = self.p_animations[self.status][self.p_animation_index]
        self.rect = self.image.get_rect(center=pos)

        # Weapon properties
        self.weapon_image = self.weapons['sword']
        self.weapon_rect = self.weapon_image.get_rect()
        self.particle_image = self.weapons['sword-particles']
        self.particle_reect = self.particle_image.get_rect()


    def import_assets(self):
        self.p_animations = {
            'idle': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/idle_{i}.png')).convert_alpha(), (image.get_width() * self.p_scale_factor, image.get_height() * (self.p_scale_factor + 0.2))) for i in range(1, 3)],
            'idle-up': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/idle_up_{i}.png')).convert_alpha(), (image.get_width() * self.p_scale_factor, image.get_height() * (self.p_scale_factor + 0.2))) for i in range(1, 4)],
            'run': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/run_{i}.png')).convert_alpha(), (image.get_width() * self.p_scale_factor, image.get_height() * (self.p_scale_factor + 0.2))) for i in range(1, 5)],
            'run-up': [pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/player1/run_up_{i}.png')).convert_alpha(), (image.get_width() * self.p_scale_factor, image.get_height() * (self.p_scale_factor + 0.2))) for i in range(1, 4)],
            'shadow': pygame.transform.scale((image:=pygame.image.load(f'./assets/characters/shadow.png').convert_alpha()), (image.get_width() * self.p_scale_factor, image.get_height() * self.p_scale_factor))
        }

        self.weapons = {
            'sword': pygame.transform.rotate(pygame.transform.scale((image:=pygame.image.load(f'./assets/weapons/stone/stone_sword_2.png').convert_alpha()), (image.get_width() * self.w_scale_factor, image.get_height() * self.w_scale_factor)), -45), # 45 degrees offset
            'sword-particles': pygame.transform.scale((image:=pygame.image.load('./assets/weapons/sword_particles.png')), (image.get_width() * self.w_scale_factor, image.get_height() * self.w_scale_factor * 1.5)) # -90 degrees offset
        }

    def animate(self):
        self.p_animation_index += self.p_animation_speed * 0.1 if self.status == 'idle' and int(self.p_animation_index) == 0 else self.p_animation_speed
        
        if self.p_animation_index >= len(self.p_animations[self.status]):
            self.p_animation_index = 0
        
        image = self.p_animations[self.status][int(self.p_animation_index)]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def movement(self):
        keys = pygame.key.get_pressed()

        if not any([keys[control] for control in self.controls.values()]):
            self.status = 'idle' if not self.facing_up else 'idle-up'

        if keys[self.controls['a']]:
            self.facing_right = False
            self.status = 'run' 
            self.direction.x = -1
        
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

        if keys[self.controls['w']]:
            self.status = 'run-up'
            self.facing_up = True
            self.direction.y = -1
        
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
        self.win.blit(self.p_animations['shadow'], self.rect.midleft - offset + Vector2(3, 20))

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

    def rotate_on_pivot(self, image: pygame.Surface, angle: float, origin: Vector2, radius: Vector2, angle_offset: float=0) -> tuple:
        """
        Note: angle and angle_offset are for counter-clockwise rotation
        """
        angle += angle_offset

        surf = pygame.transform.rotate(image, angle) # rotates angle counter-clockwise (full 360 is just rotating 180 counter-clockwise and -180 counter-clockwise, which is just 180 clockwise)

        new_rotated_point = origin + radius.rotate(-angle) # origin point + coords of radius that intersects with the circle given an angle (think about the unit circle, except the radius may not be 1)
        rect = surf.get_rect(center = new_rotated_point) # creates the rect surface where the rotated image gets centered on new_rotated_point (a point that lies on the circle that has its origin at the origin's center)

        return surf, rect
    
    def update_player_direction(self):
        self.facing_right = True if self.pos.x > self.origin.x else False
        self.facing_up = True if self.pos.y < self.origin.y else False

    def draw_sword(self, angle):
        image = self.weapon_image
        image, self.weapon_rect = self.rotate_on_pivot(image, angle, self.origin, Vector2(60, 0), angle_offset=90 * self.sword_direction)
        self.win.blit(image, self.weapon_rect)

    def draw_sword_particles(self, angle):
            particle_image = pygame.transform.flip(self.particle_image, True, False) if self.sword_direction == 1 else pygame.transform.flip(self.particle_image, True, True)
            particle_image, self.particle_rect = self.rotate_on_pivot(particle_image, angle, self.origin, Vector2(45, -20 if self.sword_direction == 1 else 20))
            self.win.blit(particle_image, self.particle_rect)

    def sword_mechanics(self, offset):

        if pygame.mouse.get_pressed()[0] and not self.triggered and not self.clicked:
            self.clicked = True
            self.triggered = True
            self.origin = Vector2(self.rect.center - offset)
            self.pos = Vector2(pygame.mouse.get_pos())
        
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False
        
        if self.triggered:
            if self.w_counter > self.w_delay:
                self.triggered = False
                self.w_counter = 0
                self.sword_direction *= -1
                return
            
            self.w_counter += 0.1

            mouse_offset = self.pos - self.origin # essentially creates a cartesian plane where the origin is at the center of the player (except y value is reversed)
            angle = -degrees(atan2(mouse_offset.y, mouse_offset.x)) # since the value of y is reversed, the output will always be reversed, that's why there is a negative sign in front

            self.draw_sword(angle)
            self.draw_sword_particles(angle)

    def update(self, offset: Vector2):
        self.sword_mechanics(offset)
        self.update_player_direction()
        self.draw_shadow(offset)
        self.draw_player(offset)
        self.movement()        
        self.animate()
        