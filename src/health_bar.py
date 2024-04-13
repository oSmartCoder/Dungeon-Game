import pygame
from pygame.math import Vector2

class HealthBar:
    def __init__(self, pos: tuple[float, float], health: int):

        self.win = pygame.display.get_surface()

        self.colours = {
            'red': (215, 59, 74),
            'orange': (),
            'green': (67, 186, 64)
        }
        self.scale_factor = 6

        self.image = pygame.transform.scale((img:=pygame.image.load('./assets/gui/health bar/health_bar.png').convert_alpha()), (img.get_width() * self.scale_factor, img.get_height() * self.scale_factor))

        self.template_rect = self.image.get_rect(topleft=pos)

        self.health_rect = pygame.Rect(*(self.template_rect.topleft + Vector2(2, 2) * self.scale_factor), self.template_rect.width * 9 / 10, self.template_rect.height * 5 / 9)

        self.health = health

    
    def display_text(self, text: str, pos: tuple[int, int], font_size: int=30, colour: str='white'):
        font = pygame.font.Font('./assets/fonts/font.ttf', font_size)
        image = font.render(text, True, colour)
        self.win.blit(image, image.get_rect(center=pos).topleft + Vector2(0, 4))


    def update(self):
        self.win.blit(self.image, self.template_rect)
        pygame.draw.rect(self.win, self.colours['green'], self.health_rect)

        self.display_text('15/20', self.health_rect.center)
        