from abc import ABC, abstractmethod
import pygame

class Obstacle(ABC):
    def __init__(self, x, y, width, height):
        self._rect = pygame.Rect(x, y, width, height)

    @abstractmethod
    def draw(self, screen, camera_x):
        pass

    @abstractmethod
    def update(self):
        pass

    def get_rect(self):
        return self._rect