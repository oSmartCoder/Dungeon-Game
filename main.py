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

        self.game = Game()
    
    def update(self):
        self.game.update()

    def run(self):
        while True:
            self.update()

            pygame.display.update()

            self.CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    main = Main()
    main.run()