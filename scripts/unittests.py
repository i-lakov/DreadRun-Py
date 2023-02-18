import unittest
import pygame
from player import Player
from level import Level
from settings import *

class TestPlayer(unittest.TestCase):
    def test_player_hurt(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        player = Player((0, 0), None)
        old_health = Player.health
        player.damage_taken()
        self.assertLess(Player.health, old_health)

    def test_player_ammo(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        old_ammo = Player.bullets
        player.shot_fired()
        self.assertLess(Player.bullets, old_ammo)

    def test_player_y_direction_initial(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        self.assertEqual(player.direction.y, 0)

    def test_player_jump(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        player.jump()
        self.assertNotEqual(player.direction.y, 0)

    def test_player_x_direction_initial(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        self.assertEqual(player.direction.x, 0)

    def test_player_dies_falling(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        player.rect.y = screen_height + 1000
        player.update()
        self.assertEqual(Player.is_alive, False)

    def test_player_dies_damage(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        player = Player((0, 0), level.create_explosion)
        Player.health = 1
        player.damage_taken()
        self.assertEqual(Player.is_alive, False)

class TestLevel(unittest.TestCase):
    def test_level_should_collide(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        self.assertEqual(level.should_collide('plant'), False)
        self.assertEqual(level.should_collide('chest'), False)
        self.assertEqual(level.should_collide('spikes'), False)
        self.assertEqual(level.should_collide('grass'), True)
        self.assertEqual(level.should_collide('dirt'), True)
        self.assertEqual(level.should_collide('box'), True)

    def test_level_should_damage_player(self):
        pygame.init()
        screen = pygame.display.set_mode((screen_width, screen_height))
        level = Level(screen)
        self.assertEqual(level.should_damage('plant'), False)
        self.assertEqual(level.should_damage('chest'), False)
        self.assertEqual(level.should_damage('spikes'), True)
        self.assertEqual(level.should_damage('grass'), False)
        self.assertEqual(level.should_damage('dirt'), False)
        self.assertEqual(level.should_damage('box'), False)


if __name__ == "__main__":
    unittest.main()