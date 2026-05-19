from abc import ABC, abstractmethod
import pygame
from Setting import *

class Character(ABC):
    def __init__(self, x, y, width, height, hp, speed):
        self._rect = pygame.Rect(x, y, width, height)
        self.__hp = hp
        self._speed = speed
        self._vel_y = 0
        self._on_ground = False
        self._direction = 1

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def draw(self, screen, camera_x):
        pass

    def apply_gravity(self):
        self._vel_y += GRAVITY
        self._rect.y += self._vel_y

    def take_damage(self, damage):
        self.__hp -= damage

    def get_hp(self):
        return self.__hp

    def set_hp(self, hp):
        self.__hp = hp

    def is_dead(self):
        return self.__hp <= 0

    def get_rect(self):
        return self._rect