from csv import reader
from os import walk
import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    # Go through each file and create full paths to just the image info nothing else.
    for _, __, img_files in walk(path):
        for image in img_files:
            # Sort list to allow object to be placed in proper areas of map with the right amount placed.
            img_files.sort()
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list
