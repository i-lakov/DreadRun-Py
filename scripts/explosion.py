import pygame
from helper import import_folder

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self._frame_index = 0
        self._animation_speed = 0.2
        self._frames = import_folder('assets/explosion')
        self.image = self._frames[self._frame_index]
        self.rect = self.image.get_rect(center = pos)

    """Handles all the animations to do an explosion."""
    def animate(self):
        self._frame_index += self._animation_speed
        if self._frame_index >= len(self._frames):
            self.kill()
        else:
            self.image = self._frames[int(self._frame_index)]

    """Normal pygame update function, invoked every frame."""
    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift