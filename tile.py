import pygame
from settings import *


# CLass for empty positions in game map.
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, groups, sprite_type, surface=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        # Type of sprite. i.e. enemy, obstacle...
        self.sprite_type = sprite_type
        # Image based on the surface parameter, default is a black surface.
        self.image = surface
        if self.sprite_type == "object":
            # Do an offset for size of larger objects .
            self.rect = self.image.get_rect(topleft=(position[0], position[1] - TILE_SIZE))
        else:
            # Rectangle of the tiles.
            self.rect = self.image.get_rect(topleft=position)
        # Set hit box to be slightly smaller than the rectangle.
        self.hit_box = self.rect.inflate(0, -10)
