import pygame
import time
from helper import import_folder
from score import Score
from settings import screen_height, damage_cooldown, explosion_cooldown

class Player(pygame.sprite.Sprite):
    is_alive = True
    health = 3
    bullets = 3

    def __init__(self, pos, create_explosion):
        super().__init__()
        self.import_assets()
        self.import_sound()

        # player animation
        self._frame_index = 0
        self._animation_speed = 0.1

        # explosion animation
        self.create_explosion = create_explosion

        self.image = self.animations['idle'][self._frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self._score = Score()

        # taking damage
        self._damage_time = 0
        self._damage_locked = False
        # dealing damage (explosion)
        self._explos_time = 0
        self._explos_locked = False

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.default_speed = 6
        self.speed = 6
        self.gravity = 0.8
        self._jump_force = -16
        self._knockback_force = -32
        self._can_double_jump = True

        # Animation related
        self._status = 'idle'
        self._right_face = True
        self.on_ground = True
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    """Checks whether we can take damage and applies it."""
    def damage_taken(self):
        if self._damage_locked:
            time_now = time.time()
            if time_now - self._damage_time > damage_cooldown:
                self._damage_locked = False
        else:
            self._damage_time = time.time()
            self._damage_locked = True
            Player.health -= 1
            if Player.health == 0:
                self.die()
    
    def die(self):
        Player.is_alive = False

    """Checks whether we can actually perform an explosion and applies knockback."""
    def shot_fired(self):
        if self._explos_locked:
            time_now_explos = time.time()
            if time_now_explos - self._explos_time > explosion_cooldown:
                self._explos_locked = False
        else:
            self._explos_time = time.time()
            self._explos_locked = True
            if Player.bullets >= 0:
                Player.bullets -= 1
                self.create_explosion(self.rect.midbottom)
                self.knockback()

    """Helper function to import necessary textures."""
    def import_assets(self):
        path = 'assets/player/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}

        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    """Helper function to import necessary sounds."""
    def import_sound(self):
        path = 'assets/sounds/jump.wav'
        self._jump_sound = pygame.mixer.Sound(path)

    """Handles the animation of the player."""
    def animate(self):
        animation = self.animations[self._status]

        self._frame_index += self._animation_speed
        if self._frame_index >= len(animation):
            self._frame_index = 0
        
        sprite = animation[int(self._frame_index)]
        if self._right_face:
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

    """Receives input by key events and applies it."""
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            self.direction.x = 1
            self._right_face = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self._right_face = False
        else:
            self.direction.x = 0
    
        if keys[pygame.K_SPACE]:
            if self.on_ground:
                pygame.mixer.Sound.play(self._jump_sound)
                self.jump()
                self._can_double_jump = True
            elif self._status == 'fall' and self._can_double_jump:
                pygame.mixer.Sound.play(self._jump_sound)
                self.jump()
                self._can_double_jump = False
        
        if keys[pygame.K_e]:
            self.shot_fired()

    """Differentiates between different animation states."""
    def get_anim_state(self):
        if self.direction.y < 0:
            self._status = 'jump'
        elif self.direction.y > self.gravity + 0.1: # because of reset of gravity in level class
            self._status = 'fall'
        else:
            if self.direction.x != 0:
                self._status = 'run'
            else:
                self._status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    """Perform the jump action."""
    def jump(self):
        self.direction.y = self._jump_force

    """Perform the knockback effect of using the weapon."""
    def knockback(self):
        self.direction.y = self._knockback_force

    """Normal pygame update function, invoked every frame."""
    def update(self):
        self.get_input()
        self.get_anim_state()
        self.animate()
        if self.direction.x > 0 and not self.on_left and not self.on_right:
            self._score.receive_pos(self.direction.x)

        if self.rect.y > screen_height:
            self.die()