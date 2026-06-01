import pygame
import time
from Weapon.Standar import StandardWeapon
from Char.Character import Character
from Setting import *

class Player(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 70, 100, 5)

        self.__weapon = StandardWeapon()
        self.__upgrade_timer = 0
        self.__laser_active = False

        self.__damage_bonus = 0
        self.__fire_rate_bonus = 0.0
        self.__max_hp = 100

    def move(self, keys=None):
        if keys[pygame.K_a]:
            self._rect.x -= self._speed
            self._direction = -1

        if keys[pygame.K_d]:
            self._rect.x += self._speed
            self._direction = 1

    def jump(self):
        if self._on_ground:
            self._vel_y = -15
            self._on_ground = False

    def attack(self, bullets, target_pos):
        self.__weapon.shoot(self, bullets, target_pos)

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, BLUE, (
            self._rect.x - camera_x,
            self._rect.y,
            self._rect.width,
            self._rect.height
        ))

        hp_width = self.get_hp() * 2
        pygame.draw.rect(screen, RED, (20, 20, 200, 20))
        pygame.draw.rect(screen, GREEN, (20, 20, hp_width, 20))

        if self.__laser_active:
            pygame.draw.rect(
                screen,
                PURPLE,
                (
                    self._rect.centerx - camera_x,
                    self._rect.centery - 6,
                    40,
                    12
                )
            )
            self.__laser_active = False

    def set_weapon(self, weapon):
        self.__weapon = weapon
        self.__upgrade_timer = time.time()

    def update_weapon(self):
        if (
            time.time() - self.__upgrade_timer >= 15
            and not isinstance(self.__weapon, StandardWeapon)
        ):self.__weapon = StandardWeapon()

    def activate_laser(self, target_pos, damage):
        self.__laser_active = True

    def get_weapon(self):
        return self.__weapon
    
    def set_damage_bonus(self, bonus):
        self.__damage_bonus = bonus
 
    def get_damage_bonus(self):
        return self.__damage_bonus
 
    def set_fire_rate_bonus(self, bonus):
        self.__fire_rate_bonus = bonus
 
    def get_fire_rate_bonus(self):
        return self.__fire_rate_bonus
 
    def set_max_hp(self, max_hp):
        self.__max_hp = max_hp
 
    def get_max_hp(self):
        return self.__max_hp