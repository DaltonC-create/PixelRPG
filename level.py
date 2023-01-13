import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug


class Level:
    def __init__(self):

        # Get the display surface.
        self.player = None
        self.display_surface = pygame.display.get_surface()

        # Sprite group setup.
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        # update & draw the game.
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
