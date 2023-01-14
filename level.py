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
        # Loop over WORLD_MAP for columns & rows.
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                # Set spacing between each index according to the tile size.
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                # The value at the current index is an x, then it's an obstacle.
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                # The value at the current index is a p, so it is the player.
                if col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

    # Runs the level class.
    def run(self):
        # update & draw the game.
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Get half the width & height of the display surface.
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # Vector to help offset the camera according to player position.
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Getting the offset.
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in self.sprites():
            # Setting the offset position to the top left according to values in offset vector.
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
