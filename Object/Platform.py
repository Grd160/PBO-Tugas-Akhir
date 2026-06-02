import pygame
from Object.Obstacle import Obstacle
from Setting import GRAY

class Platform(Obstacle):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

        self.image = pygame.image.load(
            "Assets/Patform/tileset.png"
        ).convert_alpha()

    def draw(self, screen, camera_x):
        tile_width = self.image.get_width()
        tile_height = self.image.get_height()

        # Ulangi gambar sepanjang platform
        for x in range(0, self._rect.width, tile_width):
            screen.blit(
                self.image,
                (
                    self._rect.x - camera_x + x,
                    self._rect.y
                )
            )

    def update(self):
        pass