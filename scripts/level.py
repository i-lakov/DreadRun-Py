import random
import pygame
from tiles import Tile
from settings import *
from player import Player
from enemy import Enemy
from perlin_noise import PerlinNoise
from explosion import Explosion

class Level:
    def __init__(self, surface):
        self._display_surface = surface
        self._level = []
        self._chunk_size = 200
        self.level_generator()
        self.setup()
        self._world_shift = 0
        self._cur_x = 0

        # explosion related
        self._explosion_sprite = pygame.sprite.GroupSingle()

    """Handles the creation of the explosion animation and killing of nearby enemies."""
    def create_explosion(self, pos):
        explosion_sprite_animation = Explosion(pos)
        self._explosion_sprite.add(explosion_sprite_animation)

        for enemy_indiv in self._enemies:
            enemy = enemy_indiv.sprite
            if self._explosion_sprite.sprite.rect.colliderect(enemy.rect):
                enemy.rect.y = screen_height + 1    # move enemy below surface, so it can self handle its death

    def setup(self):
        self._tiles = pygame.sprite.Group()
        self._player = pygame.sprite.GroupSingle()
        self._enemies = []

        for r_index, row in enumerate(self._level):
            for b_index, box in enumerate(row):
                x = b_index * tile_size
                y = r_index * tile_size

                if box == 'G':
                    tile = Tile((y, x), tile_size, 'grass')
                    self._tiles.add(tile)
                elif box == 'D':
                    tile = Tile((y, x), tile_size, 'dirt')
                    self._tiles.add(tile)
                elif box == 'H':
                    tile = Tile((y, x), tile_size, 'plant')
                    self._tiles.add(tile)
                elif box == 'S':
                    tile = Tile((y, x), tile_size, 'spikes')
                    self._tiles.add(tile)
                elif box == 'B':
                    tile = Tile((y, x), tile_size, 'box')
                    self._tiles.add(tile)
                elif box == 'C':
                    tile = Tile((y, x), tile_size, 'chest')
                    self._tiles.add(tile)
                elif box == 'P':
                    player_sprite = Player((y, x), self.create_explosion)
                    self._player.add(player_sprite)
                elif box == 'E':
                    enemy = pygame.sprite.GroupSingle()
                    enemy_sprite = Enemy((y, x))
                    enemy.add(enemy_sprite)
                    self._enemies.append(enemy)

    """Simulates a camera effect, as there's no global space in pygame."""
    def camera_effect(self):
        player = self._player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width * 1/3 and direction_x < 0:
            self._world_shift = 8
            player.speed = 0
        elif player_x > screen_width * 2/3 and direction_x > 0:
            self._world_shift = -8
            player.speed = 0
        else:
            self._world_shift = 0
            player.speed = player.default_speed

    """Performs checks to determine whether the player or enemies are colliding with anything on the x axis."""
    def horizontal_collision(self):
        # enable player to move horizontally
        player = self._player.sprite
        player.rect.x += player.direction.x * player.speed

        # enable enemies to move horizontally
        for enemy_indiv in self._enemies:
            enemy = enemy_indiv.sprite
            enemy.rect.x += enemy.direction.x * enemy.speed

        # only player has horizontal collision
        for sprite in self._tiles.sprites():
            if self.should_damage(sprite.get_name()) and sprite.rect.colliderect(player.rect):
                    player.damage_taken()
            if self.should_collide(sprite.get_name()) and sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:  # leftwards collision
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self._cur_x = player.rect.left
                if player.direction.x > 0:  # rightwards collision
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self._cur_x = player.rect.right

        if player.on_left and (player.rect.left < self._cur_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self._cur_x or player.direction.x <= 0):
            player.on_right = False

    """Performs checks to determine whether the player or enemies are colliding with anything on the y axis.
    Applies gravity.
    """
    def vertical_collision(self):
        player = self._player.sprite
        player.apply_gravity()      

        for enemy_indiv in self._enemies:
            enemy = enemy_indiv.sprite
            enemy.apply_gravity()

            for sprite in self._tiles.sprites():
                if ( self.should_damage(sprite.get_name()) and sprite.rect.colliderect(player.rect) ) or ( enemy.rect.colliderect(player.rect) ):
                        player.damage_taken()
                if self.should_collide(sprite.get_name()) and sprite.rect.colliderect(player.rect):
                    if player.direction.y < 0:  # 'head' collision
                        player.rect.top = sprite.rect.bottom
                        # gravity increases constantly, so reset it
                        player.direction.y = 0
                        player.on_ceilling = True
                    elif player.direction.y > 0:  # 'feet' collision
                        player.rect.bottom = sprite.rect.top
                        player.direction.y = 0
                        player.on_ground = True
                if self.should_collide(sprite.get_name()) and sprite.rect.colliderect(enemy.rect):
                    if enemy.direction.y < 0:
                        enemy.rect.top = sprite.rect.bottom
                        enemy.direction.y = 0
                        enemy.on_ceiling = True
                    elif enemy.direction.y > 0:
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                        enemy.on_ground = True

            if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity + 0.1:
                player.on_ground = False
            if player.on_ceiling and player.direction.y > 0:
                player.on_ceiling = False

            if enemy.on_ground and enemy.direction.y < 0 or enemy.direction.y > enemy.gravity + 0.1:
                enemy.on_ground = False
            if enemy.on_ceiling and enemy.direction.y > 0:
                enemy.on_ceiling = False

    def should_collide(self, tile):
        if tile == 'plant' or tile == 'spikes' or tile == 'chest':
            return False
        return True

    def should_damage(self, tile):
        if tile == 'spikes':
            return True
        return False

    """Draws all necessary sprites, used by the level, to the screen.
    Also handles the collisions of player and enemies.
    """
    def draw(self):
        self._tiles.update(self._world_shift)
        self._tiles.draw(self._display_surface)
        self.camera_effect()
        
        # explosion related
        self._explosion_sprite.update(self._world_shift)
        self._explosion_sprite.draw(self._display_surface)

        self._player.update()
        for enemy_indiv in self._enemies:
            enemy_indiv.update(self._world_shift)
        self.horizontal_collision()
        self.vertical_collision()
        self._player.draw(self._display_surface)
        for enemy_indiv in self._enemies:
            enemy_indiv.draw(self._display_surface)
    
    """Handles the unique level generation, using perlin noise."""
    def level_generator(self):
        frequency = 0.05
        height_multiplier = 30
        height_addition = 6
        first_block_height = 0
        first_block_height_written = False
        player_block_height = 0

        for x in range(self._chunk_size):
            noise = PerlinNoise()
            height = int(abs(noise(x * frequency) * height_multiplier) + height_addition)
            if not first_block_height_written:
                first_block_height_written = True
                first_block_height = height
            if x == player_start_pos:
                player_block_height = height - 2    # 1 block above starting chest
            
            column = []
            for y in range(level_height):
                if y < height - 1:
                    column.append(' ')  # air
                elif y == height - 1:   # above surface block
                    if x == player_start_pos:
                        column.append('C')  # start chest
                    elif random.randint(0, 10) > 6:
                        column.append('H')  # hedge
                    elif random.randint(0, 10) > 7:
                        column.append('S')  # spikes
                    elif random.randint(0, 15) > 13:
                        column.append('E')  # enemy
                    else:
                        column.append(' ')
                elif y == height:   # surface block
                    column.append('G')  # grass
                else:               # below surface
                    column.append('D')  # dirt

            self._level.append(column)
        
        self._level[player_start_pos][player_block_height] = 'P'     # player
        
        # boxes to prevent you from accidentally falling at start
        for i in range(player_start_pos):
            for j in range(8):
                self._level[i][first_block_height + 3 - j] = 'B' 
