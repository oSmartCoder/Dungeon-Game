import pygame
from pygame.locals import *
import sys

from settings import *
from support import display_text
from src import Game
from src import Menu



class Main:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Dungeon Game')
        self.CLOCK = pygame.time.Clock()

        self.win = pygame.display.set_mode((WIN_X, WIN_Y))
        pygame.display.set_icon(pygame.image.load('./assets/gui/icon.png'))

        # Custom cursor setup
        self.cursor = pygame.image.load('./assets/gui/cursor/white.png')

        self.game = Game()
        self.menu = Menu()


    def update(self):
        if self.menu.in_menu:
            self.menu.play_music()
            self.menu.update()
        else:
            if self.game.victory:
                self.display_victory_screen()
            elif self.game.game_over:
                self.display_game_over_screen()
            elif not self.game.game_over:
                self.game.play_music()
                self.game.update()
    
    def display_game_over_screen(self):
        display_text(self.win, 'Game Over', (WIN_X / 2, WIN_Y / 4), font_name='yoster', font_size=100)
    
    def display_victory_screen(self):
        display_text(self.win, 'You Win!', (WIN_X / 2, WIN_Y / 4), font_name='yoster', font_size=100)


    def display_cursor(self):
        pos = pygame.mouse.get_pos()
        self.win.blit(self.cursor, pos)

    def run(self):
        while True:
            self.win.fill(COLOURS['background'])
            
            self.update()

            self.CLOCK.tick(FPS)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    main = Main()
    main.run()