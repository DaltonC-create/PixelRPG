import pygame
from settings import *


# CLass for empty positions in game map.
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.image.load("graphics/test/rock.png").convert_alpha()
        # Rectangle of the tiles.
        self.rect = self.image.get_rect(topleft=position)
        # Set hit box to be slightly smaller than the rectangle.
        self.hit_box = self.rect.inflate(0, -10)
