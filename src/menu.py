import pygame
from pygame.locals import *
from pygame.mixer import Sound

from settings import *
from support import display_text
from decorators import run_once


class Menu:
    def __init__(self):
        self.win = pygame.display.get_surface()

        self.import_images()
        self.import_sounds()

        self.in_menu = True
        self.hover = False
        self.clicked = False

        self.page = 'main'

    def import_images(self):
        self.background_image = pygame.transform.scale(pygame.image.load('./assets/background gradient.png'), (WIN_X, WIN_Y))

    @run_once
    def play_music(self):
        self.music = Sound('./assets/sounds/music/space groove.mp3')
        self.music.set_volume(0.5)
        self.music.play(loops=-1, fade_ms=1000)

    def import_sounds(self):
        self.click_sound = Sound('./assets/sounds/ui/click.wav')
        self.menu_close_sound = Sound('./assets/sounds/ui/menu close.wav')
        self.menu_open_sound = Sound('./assets/sounds/ui/menu open.wav')
        self.select_sound = Sound('./assets/sounds/ui/select.wav')

        self.click_sound.set_volume(0.5)
        self.select_sound.set_volume(0.5)

    def display_title(self):
        display_text(self.win, 'Dungeon Game', (WIN_X / 2, WIN_Y / 4), font_name='yoster', font_size=80)

    def options(self):
        pos = pygame.mouse.get_pos()

        for i, text_rect in enumerate((options:=[display_text(self.win, option, (WIN_X / 2, 350 + 90 * i), font_name='font', font_size=50) for i, option in enumerate(['PLAY', 'SHOP', 'SETTINGS'])])):
            # if above may seem perplexing, the for loop is really just displaying all the diff options available and since display_text() returns the text rect, we can use that to check for mouse collision etc.
            if text_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] and not self.clicked:
                    self.click_sound.play()
                    self.clicked = True
                
                if pygame.mouse.get_pressed()[0] and self.clicked:
                    match i:
                        case 0:
                            self.in_menu = False
                            self.music.fadeout(500)
                        case 1:
                            print('This feature is still under development!')

                        case 2:
                            print('This feature is still under development!')

                        case _:
                            raise ValueError                    
                    return
                
                if not pygame.mouse.get_pressed()[0] and self.clicked:
                    self.clicked = False
                
                if not self.hover:
                    self.hover = True
                    self.select_sound.play()
        
        if not any([text_rect.collidepoint(pos) for text_rect in options]):
            self.hover = False


    def update(self):
        self.win.blit(self.background_image, (0, 0))
        self.display_title()
        self.options()