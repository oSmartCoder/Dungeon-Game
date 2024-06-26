import pygame
from pygame.math import Vector2
from pygame.mixer import Sound

import json
from math import degrees, atan2

from settings import *
from support import display_text


class Player(pygame.sprite.Sprite):
    """
        Note: Parent classes of Player (groups) access delta, direction, image, and rect for external calculation and value modification
    """
    def __init__(self, pos: tuple, groups: pygame.sprite.Group):
        super().__init__(groups)

        self.win = pygame.display.get_surface()

        # Player setup
        self.p_scale_factor = 4
        self.p_animation_index = 0
        self.p_animation_speed = 0.15
        self.delta = Vector2()

        # Import player and weapon data
        self.import_data()

        # Weapon setup
        self.w_scale_factor = 3.5
        self.w_animation_counter = 0
        self.w_animation_period = 1.5
        self.w_delay = 1
        self.w_delay_counter = self.w_delay
        self.triggered = False
        self.sword_direction = 1
        self.origin, self.pos = Vector2(), Vector2()
        self.clicked = False
        self.disable_controls = False
        
        # Weapon stats
        self.damage = self.weapon_data['stone']['sword']['damage']

        # Player stats
        self.initial_health = self.player_data['health']
        self.health = self.player_data['health']
        self.knockback = self.player_data['knockback']
        self.invincibility_cooldown = self.player_data['invincibility cooldown']

        # Player controls
        self.vel = 6
        self.controls = {
            'a': pygame.K_a,
            'd': pygame.K_d,
            's': pygame.K_s,
            'w': pygame.K_w
        }

        # Load assets
        self.import_images()
        
        # Player properties
        self.direction = Vector2()
        self.facing_right = True
        self.facing_up = False
        self.status = 'idle'
        self.image = self.p_animations[self.status][self.p_animation_index]
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.got_attacked = False
        
        self.invincibility_counter = 0

        # Player attributes
        self.coins = 0

        # Weapon properties
        self.weapon_image = self.weapons['sword']
        self.particle_images = self.weapons['sword-particles']

        # Health Bar
        self.hb_scale_factor = 3
        self.hb_image = pygame.transform.scale((image:=pygame.image.load('./assets/gui/health bar/health_bar.png').convert_alpha()), (image.get_width() * self.hb_scale_factor, image.get_height() * self.hb_scale_factor))
        self.hb_template_rect = self.hb_image.get_rect(topleft=(20, 20))
        
        self.health_bar_rect = pygame.Rect(*(self.hb_template_rect.topleft + Vector2(3, 3) * self.hb_scale_factor), self.hb_template_rect.width * 12 / 13, self.hb_template_rect.height * 5 / 8)
        self.health_rect = self.health_bar_rect.copy()

        # Load Sounds
        self.import_sounds()

    def import_images(self):
        self.p_animations = {
            'idle': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/idle_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2)) for i in range(1, 3)],
            'idle-up': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/idle_up_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2)) for i in range(1, 2)],
            'run': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/run_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2)) for i in range(1, 5)],
            'run-finish': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/run_finish_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2)) for i in range(1, 4)],
            'run-up': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/run_up_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2))for i in range(1, 4)],
            'run-up-finish': [pygame.transform.scale_by(pygame.image.load(f'./assets/characters/player1/run_up_finish_{i}.png').convert_alpha(), (self.p_scale_factor, self.p_scale_factor + 0.2)) for i in range(1, 4)],
        }

        self.weapons = {
            'sword': pygame.transform.rotate(pygame.transform.scale_by(pygame.image.load(f'./assets/weapons/stone/stone_sword_2.png').convert_alpha(), self.w_scale_factor), -45), # 45 degrees offset
            'sword-particles': [pygame.transform.scale_by(pygame.image.load(f'./assets/weapons/sword_particles_{i}.png'), self.w_scale_factor) for i in range(1, 3)] # -90 degrees offset
        }

    def import_sounds(self):
        self.sword_sound = Sound('./assets/sounds/items/sword.wav')
        self.player_roll_sound = Sound('./assets/sounds/player/player_roll.wav')
        # self.footsteps_sound = Sound('./assets/sounds/player/footsteps.wav')

    def import_data(self):
        # Import weapon data
        with open('./data/weapon_data.json') as rf:
            self.weapon_data = json.load(rf)

        # Import player data
        with open('./data/player_data.json') as rf:
            self.player_data = json.load(rf)      

    def animate(self):
        self.p_animation_index += self.p_animation_speed * 0.1 if self.status == 'idle' and int(self.p_animation_index) == 0 else self.p_animation_speed

        if self.p_animation_index >= len(self.p_animations[self.status]):
            self.p_animation_index = 0
            
            match self.status:
                case 'run-finish':
                    self.status = 'idle'

                case 'run-up-finish':
                    self.status = 'idle-up'
        
        image = self.p_animations[self.status][int(self.p_animation_index)]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        if self.got_attacked:
            if int(self.invincibility_counter * 10) % 6 == 0:
                self.image.set_alpha(80)
            else:
                self.image.set_alpha(200)
        else:
            self.image.set_alpha(255)

        self.mask = pygame.mask.from_surface(self.image)

    def user_input(self):
        if self.disable_controls:
            return

        keys = pygame.key.get_pressed()

        self.delta = Vector2()

        if not any([keys[control] for control in self.controls.values()]):
            match self.status:
                case 'run' if not self.facing_up:
                    self.status = 'run-finish'
                case 'run-up' if self.facing_up:
                    self.status = 'run-up-finish'
            return
        
        if any([keys[control] for control in self.controls.values()]):
            pass

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
        
        if any((keys[self.controls['a']], keys[self.controls['d']])) and not keys[self.controls['w']]:
            self.status = 'run'
            self.facing_up = False

        # Normalise vector movement (so that diagonal movement won't go 41% faster)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.delta += self.direction * self.vel         

    def draw_player(self, offset):
        self.win.blit(self.image, self.rect.topleft - offset)

    def rotate_on_pivot(self, image: pygame.Surface, angle: float, origin: Vector2, radius: Vector2, angle_offset: float=0) -> tuple:
        """
        Note: angle and angle_offset are for counter-clockwise rotation
        """
        angle += angle_offset

        surf = pygame.transform.rotate(image, angle) # rotates angle counter-clockwise (full 360 is just rotating 180 counter-clockwise and -180 counter-clockwise, which is just 180 clockwise)

        new_rotated_point = origin + radius.rotate(-angle) # origin point + coords of radius that intersects with the circle given an angle (think about the unit circle, except the radius may not be 1)
        rect = surf.get_rect(center = new_rotated_point) # creates the rect surface where the rotated image gets centered on new_rotated_point (a point that lies on the circle that has its origin at the origin's center)

        return surf, rect
    
    def update_direction_from_delta(self, inverse_facing_right=False):
        if self.delta.x > 0:
            self.facing_right = True if not inverse_facing_right else False
            self.direction.x = 1
        elif self.delta.x < 0:
            self.facing_right = False if not inverse_facing_right else True
            self.direction.x = -1
        
        if self.delta.y > 0:
            self.direction.y = 1
        elif self.delta.y < 0:
            self.direction.y = -1

    def update_player_direction_and_animation_status(self):
        self.facing_right = True if self.pos.x > self.origin.x else False
        self.facing_up = True if self.pos.y < self.origin.y else False

        self.direction.x = 1 if self.facing_right else -1
        self.direction.y = 1 if not self.facing_up else -1

        match self.status:
            case 'idle' if self.facing_up:
                self.status = 'idle-up'
            case 'run' if self.facing_up:
                self.status = 'run-up'
            case 'idle-up' if not self.facing_up:
                self.status = 'idle'
            case 'run-up' if not self.facing_up:
                self.status = 'run'
        
        self.status = 'run-up' if self.facing_up else 'run'

    def draw_sword(self, angle: float):
        image = self.weapon_image
        image, self.weapon_rect = self.rotate_on_pivot(image, angle, self.origin, Vector2(60, 0), angle_offset=90 * self.sword_direction)
        self.win.blit(image, self.weapon_rect)

    def draw_sword_particles(self, angle: float):
            particle_image = self.particle_images[round(self.w_animation_counter / self.w_animation_period)] if self.sword_direction == 1 else pygame.transform.flip(self.particle_images[round(self.w_animation_counter / self.w_animation_period)], False, True)
            particle_image, self.particle_rect = self.rotate_on_pivot(particle_image, angle, self.origin, Vector2(45, -15 if self.sword_direction == 1 else 15))
            self.particle_mask = pygame.mask.from_surface(particle_image)

            self.win.blit(particle_image, self.particle_rect)

    def add_recoil(self):
        self.delta = self.origin.move_towards(self.pos, self.vel * 3 / 4) - self.origin

    def sword_mechanics(self, offset):
        if self.w_delay_counter >= self.w_delay:
            if pygame.mouse.get_pressed()[0] and not self.triggered and not self.clicked: # Initialisation for self.triggered
                    self.clicked = True
                    self.triggered = True
                    self.disable_controls = True
                    self.origin = Vector2(self.rect.center - offset)
                    self.pos = Vector2(pygame.mouse.get_pos())
                    self.sword_sound.play()
            
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            
            if self.triggered:
                if self.w_animation_counter > self.w_animation_period:
                    self.disable_controls = False
                    self.w_delay_counter = 0
                    self.triggered = False
                    self.w_animation_counter = 0
                    self.sword_direction *= -1
                    return
                
                self.w_animation_counter += 0.1

                mouse_offset = self.pos - self.origin # essentially creates a cartesian plane where the origin is at the center of the player (except y value is reversed)
                angle = -degrees(atan2(mouse_offset.y, mouse_offset.x)) # since the value of y is reversed, the output will always be reversed, that's why there is a negative sign in front

                self.draw_sword(angle)
                self.draw_sword_particles(angle)
                self.update_player_direction_and_animation_status()
                self.add_recoil()

        else:
            self.w_delay_counter += 0.1

    def update_health_bar(self):
        self.health_rect = self.health_bar_rect.copy()
        health_percentage = self.health / self.initial_health
        self.health_rect.width = self.health_bar_rect.width * health_percentage

        if health_percentage >= 0.6:
            colour = COLOURS['green'] 
        elif health_percentage >= 0.3:
            colour = COLOURS['orange']
        else:
            colour = COLOURS['red']

        self.win.blit(self.hb_image, self.hb_template_rect)
        pygame.draw.rect(self.win, 'black', self.health_bar_rect)        
        pygame.draw.rect(self.win, colour, self.health_rect)
        display_text(self.win, f'{self.health}/{self.initial_health}', self.hb_template_rect.center + Vector2(0, 4))

    def invincibility(self, camera_sprites):
        if self.got_attacked:
            if self.invincibility_counter >= self.invincibility_cooldown:
                self.got_attacked = False
                self.invincibility_counter = 0

            else:
                if self.invincibility_counter <= self.invincibility_cooldown / 4:
                    camera_sprites.shake_camera(x_intensity=15, y_intensity=4) 
                self.invincibility_counter += 0.1

    def update(self, camera_sprites: pygame.sprite.Group):
        self.sword_mechanics(camera_sprites.offset) # self.sword_mechanics() should be ran before self.user_input() so that self.direction and self.delta values are more accurate (a change of values by one tick/frame could cause some issues/bugs with collision detection)
        self.user_input()
        self.invincibility(camera_sprites)
        self.animate()
        self.draw_player(camera_sprites.offset)
        self.update_health_bar()
        