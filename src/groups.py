import pygame
from pygame.math import Vector2
from pygame.sprite import Sprite, Group
from pygame.mixer import Sound

from random import randint, choice

from settings import *
from .tile import Coin


class CollisionGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

    def check_collision(self, active_sprite: Sprite, sprite_group: Group, direction: str, player: Sprite):
        """
        Note: All active sprites must have a delta (rate of change) and rect (sprite rect) attribute
        """

        # player 
        for sprite in sprite_group:
            if active_sprite in sprite_group:
                collision_condition = active_sprite.rect.colliderect(sprite.rect) and not player in (active_sprite, sprite) and active_sprite != sprite
            else:
                collision_condition = active_sprite.rect.colliderect(sprite.rect)
                
            if collision_condition:
                if direction == 'horizontal':
                    if active_sprite.direction.x > 0:
                        active_sprite.rect.right = sprite.rect.left
                    if active_sprite.direction.x < 0:
                        active_sprite.rect.left = sprite.rect.right
                
                elif direction == 'vertical':
                    if active_sprite.direction.y > 0:
                        active_sprite.rect.bottom = sprite.rect.top

                    elif active_sprite.direction.y < 0:
                        active_sprite.rect.top = sprite.rect.bottom

    def update_active_sprites_position(self, active_sprites: Group, player: Sprite):
        for active_sprite in active_sprites:
            active_sprite.rect.x += active_sprite.delta.x
            self.check_collision(active_sprite, self, 'horizontal', player) # check horizontal collision with collision sprites
            self.check_collision(active_sprite, active_sprites, 'horizontal', player) # check horizontal collision with own active sprites

            active_sprite.rect.y += active_sprite.delta.y
            self.check_collision(active_sprite, self, 'vertical', player) # check vertical collision with collision sprites
            self.check_collision(active_sprite, active_sprites, 'vertical', player) # check vertical collision with own active sprites


class CameraGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2()

        self.shadow_image = pygame.image.load(f'./assets/characters/shadow.png').convert_alpha()

    def center_target_camera(self, target: Sprite):
        self.offset.x = target.rect.centerx - WIN_X / 2
        self.offset.y = target.rect.centery - WIN_Y / 2
    
    def shake_camera(self, x_intensity: int | float = 10, y_intensity: int | float = 0) -> None:
        self.offset.x += choice([randint(-x_intensity, -x_intensity // 2), randint(x_intensity // 2, x_intensity)])
        self.offset.y += choice([randint(-y_intensity, -y_intensity // 2), randint(y_intensity // 2, y_intensity)])

    def draw_sprites(self, player: Sprite, active_sprites: Group):
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            if sprite in active_sprites:
                self.win.blit(pygame.transform.scale(self.shadow_image, (sprite.rect.width if sprite is player else sprite.rect.width / 1.8, sprite.rect.height / 3.5)), (sprite.rect.bottomleft - self.offset + Vector2(2 if sprite is player else 15, -10)))
            
            else:
                self.win.blit(sprite.image, offset_pos)
    
    def update_enemies(self, player: Sprite, enemy_sprites: Group):
        for sprite in enemy_sprites:
            sprite.update(player, self.offset)
    
    def update_player(self, player: Sprite):
        player.update(self)


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

        self.coin_sound = Sound('./assets/sounds/items/coin-edit.wav')
        self.victory_music = Sound('./assets/sounds/music/bit win.mp3')
        self.victory_music.set_volume(0.5)
    
    def update_collision(self, player: Sprite) -> True | False:
        for sprite in self.sprites():
            if player.rect.colliderect(sprite.rect):
                if player.mask.overlap(sprite.mask, sprite.rect.topleft - Vector2(player.rect.topleft)):
                    match sprite.layer_name:
                        case 'Coin':
                            player.coins += 1
                            self.coin_sound.play()
                            sprite.kill()

                        case 'Small Red Flask':
                            player.health += player.initial_health // 6
                            if player.health > player.initial_health:
                                player.health = player.initial_health
                            self.coin_sound.play() # Temporary until I find a sound for this
                            sprite.kill()

                        case 'Small Blue Flask':
                            player.health += player.initial_health // 6
                            if player.health > player.initial_health:
                                player.health = player.initial_health
                            self.coin_sound.play() # Temporary until I find a sound for this
                            sprite.kill()

                        case 'Chest':
                            pass

                        case 'Ladder':
                            self.victory_music.play(loops=-1, fade_ms=3000)
                            return True

                        case _:
                            pass
        
        return False
    
    def update_sprites(self, player: Sprite):
        for sprite in self.sprites():
            match sprite.layer_name:
                case 'Coin':
                    sprite.move_towards_player(player.rect.center)


class ActiveGroup(Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.enemy_hurt_sound = Sound('./assets/sounds/enemies/enemy_hurt.wav')
        self.enemy_die_sound = Sound('./assets/sounds/enemies/enemy_die.wav')

        self.player_hurt_sound = Sound('./assets/sounds/player/player_hurt.wav')
        self.player_hurt_final_sound = Sound('./assets/sounds/player/player_hurt_final.mp3')

        self.death_music = Sound('./assets/sounds/music/death_music.mp3')

    def check_collision_between_sprites(self, camera_sprites: Group, animation_sprites: Group, interactive_sprites: Group) -> True | False:
        player = self.sprites()[0]
        enemy_sprites = self.sprites()[1:]
        
        for enemy_sprite in enemy_sprites:
            if player.triggered:
                if enemy_sprite.mask.overlap(player.particle_mask, (player.particle_rect.topleft + camera_sprites.offset - enemy_sprite.rect.topleft)):
                    if enemy_sprite.health <= 0:
                        [Coin(enemy_sprite.rect.center + Vector2(randint(1, 30), randint(1, 30)), [camera_sprites, animation_sprites, interactive_sprites], 'Coin') for _ in range(enemy_sprite.coin_drops)]
                        enemy_sprite.kill()
                        self.enemy_die_sound.play()

                    elif not enemy_sprite.disable_pursue:
                        enemy_sprite.health -= player.damage
                        self.enemy_hurt_sound.play()                        
                        enemy_sprite.disable_pursue = True

                    else:
                        enemy_sprite.delta = player.origin.move_towards(player.pos, enemy_sprite.knockback) - player.origin
                        enemy_sprite.update_direction(inverse_facing_right=True)
                        camera_sprites.shake_camera(y_intensity=2)

            if enemy_sprite.triggered:
                if enemy_sprite.mask.overlap(player.mask, enemy_sprite.rect.topleft - Vector2(player.rect.topleft)):
                    if player.health <= 0:
                        player.health = 0
                        self.death_music.play()
                        return True

                    elif not player.got_attacked:
                        player.health -= enemy_sprite.damage
                        self.player_hurt_sound.play() if player.health / player.initial_health >= 0.3 else self.player_hurt_final_sound.play()
                        player.got_attacked = True

                    else:
                        player.delta = Vector2(enemy_sprite.player_delta)
                        player.update_direction_from_delta(inverse_facing_right=True)
        
        return False
