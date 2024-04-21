import pygame
from pygame.math import Vector2

FONT = './assets/fonts/font.ttf'

def display_text(surface: pygame.Surface, text: str, pos: tuple[float, float], colour: tuple[int, int, int] | str = 'white', font_size: int = 30) -> None:
    image = pygame.font.Font(FONT, font_size).render(text, True, colour)

    surface.blit(image, image.get_rect(center=pos).topleft)


