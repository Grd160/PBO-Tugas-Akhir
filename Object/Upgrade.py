import pygame
import random
from Setting import *
from Weapon.Rapid import RapidWeapon
from Weapon.Granade import GrenadeLauncher
from Weapon.Laser import LaserWeapon

class Upgrade:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.weapon_type = random.choice([
            RapidWeapon,
            GrenadeLauncher,
            LaserWeapon
        ])

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, YELLOW, (
            self.rect.x - camera_x,
            self.rect.y,
            self.rect.width,
            self.rect.height
        ))

    def get_weapon(self):
        return self.weapon_type()