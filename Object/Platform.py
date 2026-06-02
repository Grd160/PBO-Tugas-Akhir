import pygame
from Object.Obstacle import Obstacle
from Setting import GRAY

class Platform(Obstacle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.image = pygame.image.load(
            "Assets/Patform/tileset.png"
        ).convert_alpha()

        # Sesuaikan ukuran gambar dengan ukuran platform
        self.image = pygame.transform.scale(
            self.image,
            (width, height)
        )

    def draw(self, screen, camera_x):
        screen.blit(
            self.image,
            (self._rect.x - camera_x, self._rect.y)
        )

    def update(self):
        pass