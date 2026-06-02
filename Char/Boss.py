import pygame
import time
from Char.Enemy import Enemy
from Char.Character import Character
from Setting import *
from Object.Bullet import Bullet

BOSS_WIDTH  = 220
BOSS_HEIGHT = 100

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self._rect = pygame.Rect(x, y, BOSS_WIDTH, BOSS_HEIGHT)
        self.__max_hp = 500
        self.set_hp(self.__max_hp)
        self._speed = 3
        self.__direction = 1
        self.__last_shot = 0

        raw_frames = [
            pygame.image.load("Assets/Boss/enemyFlying_1.png").convert_alpha(),
            pygame.image.load("Assets/Boss/enemyFlying_2.png").convert_alpha(),
            pygame.image.load("Assets/Boss/enemyFlying_3.png").convert_alpha(),
        ]
        self.__frames = [
            pygame.transform.scale(f, (BOSS_WIDTH, BOSS_HEIGHT)) for f in raw_frames
        ]
        self.__frame_index = 0.0
        self.__anim_speed  = 0.1

    def set_hp(self, hp):
        super().set_hp(hp)
        self.__max_hp = hp

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
        self.__frame_index += self.__anim_speed
        if self.__frame_index >= len(self.__frames):
            self.__frame_index = 0.0
 
        frame = self.__frames[int(self.__frame_index)]

        if self.__direction == -1:
            frame = pygame.transform.flip(frame, True, False)
 
        screen.blit(frame, (self._rect.x - camera_x, self._rect.y))

        hp_ratio = max(0, self.get_hp() / self.__max_hp)
        hp_width = hp_ratio * 400

        pygame.draw.rect(screen, RED, (430, 20, 400, 20))
        pygame.draw.rect(screen, GREEN, (430, 20, hp_width, 20))