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
        
        self.__patrol_origin = x
        self.__patrol_range = 120
        self.__patrol_direction = 1

        raw_frames = [
            pygame.image.load("Assets/Enemy/enemyWalking_1.png").convert_alpha(),
            pygame.image.load("Assets/Enemy/enemyWalking_2.png").convert_alpha(),
        ]
        self.__frames = [
            pygame.transform.scale(f, (self._rect.width, self._rect.height)) for f in raw_frames]

        self.__frame_index = 0.0
        self.__anim_speed  = 0.1
        self.__is_moving   = False

    def move(self, player=None):
        px = player.get_rect().centerx
        py = player.get_rect().centery

        ex = self._rect.centerx
        ey = self._rect.centery

        distance = abs(px - ex)
        in_sight = distance < WIDTH and abs(py - ey) < 100

        if in_sight:
            if px > ex:
                self._rect.x += self._speed
                self._direction = 1

            else:
                self._rect.x -= self._speed
                self._direction = -1

        else:
            self._rect.x += self._speed * self.__patrol_direction

            if self._rect.x >= self.__patrol_origin + self.__patrol_range:
                self.__patrol_direction = -1

            elif self._rect.x <= self.__patrol_origin - self.__patrol_range:
                self.__patrol_direction = 1

            self._direction = self.__patrol_direction

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

    def set_fire_rate(self, rate):
        self.__fire_rate = rate

    def draw(self, screen, camera_x):
        if self.__is_moving:
            self.__frame_index += self.__anim_speed
            if self.__frame_index >= len(self.__frames):
                self.__frame_index = 0.0
        else:
            self.__frame_index = 0.0
 
        frame = self.__frames[int(self.__frame_index)]

        if self._direction == -1:
            frame = pygame.transform.flip(frame, True, False)
 
        screen.blit(frame, (self._rect.x - camera_x, self._rect.y))