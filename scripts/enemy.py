import pygame
import random
import time
from helper import import_folder
from settings import screen_height, enemy_move_time

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.time_taken = False
        self.time_started = 0
        self.action = 1

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.default_speed = 2
        self.speed = 2
        self.gravity = 0.8

        # Animation related
        self.status = 'idle'
        self.right_face = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    """Helper function to import necessary textures."""
    def import_assets(self):
        path = 'assets/enemy/'
        self.animations = {'idle': [], 'run': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    """Handles all the animations of enemy objects."""
    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        sprite = animation[int(self.frame_index)]
        if self.right_face:
            self.image = sprite
        else:
            flip_sprite = pygame.transform.flip(sprite, True, False)
            self.image = flip_sprite

        # fixing the player rectangle
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    
    """Differentiates between different animation states."""
    def get_anim_state(self):
        if self.direction.y < 0:
            pass
        elif self.direction.y > self.gravity + 0.1:     # because of reset of gravity in level class
            pass
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def die(self):
        del(self)

    """AI-like behavior for enemy movement."""
    def generate_input(self):
        if self.time_taken and time.time() - self.time_started > enemy_move_time:
            self.time_taken = False
            if self.action == 1:
                self.direction.x = 1
                self.right_face = False
            elif self.action == 2:
                self.direction.x = -1
                self.right_face = True
            elif self.action == 3:
                self.direction.x = 0

        elif not self.time_taken:
            self.time_taken = True
            self.time_started = time.time()

            self.action = random.randint(1, 3)

    """Normal pygame update function, invoked every frame"""
    def update(self, offset):
        self.generate_input()
        self.get_anim_state()
        self.animate()

        if self.rect.y > screen_height:
            self.die()

        self.rect.x += offset