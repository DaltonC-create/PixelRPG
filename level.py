import random
import pygame

from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *


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
        # dict of the different layouts of the map.
        layouts = {
            "boundary": import_csv_layout("map/map_FloorBlocks.csv"),
            "grass": import_csv_layout("map/map_Grass.csv"),
            "object": import_csv_layout("map/map_Objects.csv")
        }

        # Importing all the graphics for objects.
        graphics = {
            "grass": import_folder("graphics/grass"),
            "objects": import_folder("graphics/objects")
        }

        # Loop over dictionary containing the layouts of image.
        for style, layout in layouts.items():
            # Loop over layout for columns & rows.
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    # Avoid boundaries being placed in incorrect areas.
                    if col != "-1":
                        # Set spacing between each index according to the tile size.
                        x = col_index * TILE_SIZE
                        y = row_index * TILE_SIZE
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "grass":
                            # Get random grass image.
                            random_grass_image = random.choice(graphics["grass"])
                            # Create a grass tile.
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "grass", random_grass_image)

                        if style == "object":
                            # Create an object tile.
                            surf = graphics["objects"][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", surf)

        # Place the player in towards the middle of the screen on the path.
        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    # Runs the level class.
    def run(self):
        # update & draw the game.
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.status)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Get half the width & height of the display surface.
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # Vector to help offset the camera according to player position.
        self.offset = pygame.math.Vector2()

        # Creating the floor surface & rectangle to be below everything.
        self.floor_surf = pygame.image.load("graphics/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # Getting the offset.
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor.
        floor_offset_position = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_position)

        """
        Sort the sprites so the player appears behind it with a greater y position
        & in front of obstacles with a lesser y position.
        """
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # Setting the offset position to the top left according to values in offset vector.
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
