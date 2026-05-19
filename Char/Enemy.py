import pygame
import math
import time
from Char.Character import Character
from Setting import *
from Object.Bullet import Bullet

class Enemy(Character):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 70, 100, 2)
        self.__fire_rate = 1.2
        self.__last_shot = 0

    def move(self, player=None):
        px = player.get_rect().centerx
        py = player.get_rect().centery

        ex = self._rect.centerx
        ey = self._rect.centery

        distance = abs(px - ex)

        if distance < WIDTH and abs(py - ey) < 100:
            if px > ex:
                self._rect.x += self._speed
                self._direction = 1
            else:
                self._rect.x -= self._speed
                self._direction = -1

    def attack(self, bullets, player):
        px = player.get_rect().centerx
        py = player.get_rect().centery

        ex = self._rect.centerx
        ey = self._rect.centery

        if abs(px - ex) < WIDTH and abs(py - ey) < 100:
            current = time.time()

            if current - self.__last_shot >= self.__fire_rate:
                self.__last_shot = current

                angle = math.atan2(py - ey, px - ex)

                dx = math.cos(angle) * 7
                dy = math.sin(angle) * 7

                bullets.append(Bullet(ex, ey, dx, dy, 10, self, RED))

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, RED, (
            self._rect.x - camera_x,
            self._rect.y,
            self._rect.width,
            self._rect.height
        ))