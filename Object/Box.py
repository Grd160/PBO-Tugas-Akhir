import pygame
from Object.Obstacle import Obstacle
from Setting import ORANGE

class Box(Obstacle):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50)
        self.__hp = 50

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, ORANGE, (
            self._rect.x - camera_x,
            self._rect.y,
            self._rect.width,
            self._rect.height
        ))

    def update(self):
        pass

    def take_damage(self, damage):
        self.__hp -= damage

    def is_destroyed(self):
        return self.__hp <= 0