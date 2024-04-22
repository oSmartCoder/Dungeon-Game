import pygame
from pygame.locals import *
import sys

from settings import *
from src import Game


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

    def update(self):
        self.game.update()

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