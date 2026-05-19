import pygame
from Object.Obstacle import Obstacle
from Setting import GRAY

class Platform(Obstacle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, GRAY, (
            self._rect.x - camera_x,
            self._rect.y,
            self._rect.width,
            self._rect.height
        ))

    def update(self):
        pass