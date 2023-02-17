import pygame
from os import walk

"""Helper method to facilitate the importing of an entire folder."""
def import_folder(path):
    surfaces = []

    for _, __, sprites in walk(path):
        for sprite in sprites:
            full_path = path + '/' + sprite
            surface = pygame.image.load(full_path).convert_alpha()
            surfaces.append(surface)
    
    return surfaces