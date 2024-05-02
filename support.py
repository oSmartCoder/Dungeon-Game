import pygame

from typing import NoReturn

def display_text(surface: pygame.Surface, text: str, pos: tuple[float, float], colour: tuple[int, int, int] | str = 'white', font_name: str = 'font', font_size: int = 30, position: str = 'center') -> pygame.Rect | NoReturn:
    font = pygame.font.Font(f'./assets/fonts/{font_name}.ttf', font_size)
    image = font.render(text, True, colour)

    match position:
        case 'topleft':
            rect = image.get_rect(topleft=pos)
            surface.blit(image, rect)
            return rect

        case 'center':
            rect = image.get_rect(center=pos)
            surface.blit(image, rect)
            return rect
        
        case _:
            raise ValueError('Invalid position.')