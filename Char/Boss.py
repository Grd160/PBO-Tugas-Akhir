import pygame
import time
from Char.Enemy import Enemy
from Setting import *
from Object.Bullet import Bullet

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.set_hp(5000)
        self._speed = 3
        self.__direction = 1
        self.__last_shot = 0

    def move(self, player=None):
        self._rect.x += self._speed * self.__direction

        if self._rect.x <= MAP_WIDTH - 1200:
            self.__direction = 1

        if self._rect.x >= MAP_WIDTH - 300:
            self.__direction = -1

    def attack(self, bullets, player=None):
        current = time.time()

        if current - self.__last_shot >= 0.8:
            self.__last_shot = current

            bullets.append(Bullet(
                self._rect.centerx,
                self._rect.bottom,
                0,
                10,
                15,
                self,
                PURPLE
            ))

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, PURPLE, (
            self._rect.x - camera_x,
            self._rect.y,
            220,
            100
        ))

        hp_width = (self.get_hp() / 5000) * 400

        pygame.draw.rect(screen, RED, (430, 20, 400, 20))
        pygame.draw.rect(screen, GREEN, (430, 20, hp_width, 20))