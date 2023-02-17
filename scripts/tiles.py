import pygame
from helper import import_folder

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, texture):
        super().__init__()
        self.import_textures()
        self.name = texture
        self.image = pygame.transform.scale(self.textures[texture][0], (size, size))
        self.rect = self.image.get_rect(topleft = pos)

    """Normal pygame update function, invoked every frame."""
    def update(self, offset):
        self.rect.x += offset

    """Returns the name of the tile, can be used to differentiate between instances."""
    def get_name(self):
        return self.name

    """Helper function to import necessary textures."""
    def import_textures(self):
        path = 'assets/tiles/'
        self.textures = {'grass': [], 'dirt': [], 'plant': [], 'spikes': [], 'box': [], 'chest': []}

        for texture in self.textures.keys():
            full_path = path + texture
            self.textures[texture] = import_folder(full_path)