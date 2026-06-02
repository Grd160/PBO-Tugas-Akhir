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

        self.image = pygame.image.load(
            "Assets/Upgrade/yellowCrystal.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image,
            (self.rect.width, self.rect.height)
        )

    def draw(self, screen, camera_x):
        screen.blit(
            self.image,
            (self.rect.x - camera_x, self.rect.y)
        )

    def get_weapon(self):
        return self.weapon_type()