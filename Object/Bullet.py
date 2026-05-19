import pygame
import math
from Setting import *

class Bullet:
    def __init__(self, x, y, dx, dy, damage, owner, color=YELLOW, radius=5, max_distance=900, explosive=False, penetrate=False):
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.owner = owner
        self.color = color
        self.start_x = x
        self.start_y = y
        self.max_distance = max_distance
        self.explosive = explosive
        self.penetrate = penetrate
        self.radius_damage = 100

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen, camera_x):
        pygame.draw.rect(
            screen,
            self.color,
            (
                self.rect.x - camera_x,
                self.rect.y,
                self.rect.width,
                self.rect.height
            )
        )

    def exceeded_distance(self):
        distance = math.sqrt((self.rect.x - self.start_x) ** 2 + (self.rect.y - self.start_y) ** 2)
        return distance >= self.max_distance