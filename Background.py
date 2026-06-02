import pygame

class Background:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.width = self.image.get_width()

    def draw(self, screen, camera_x):
        start_x = -(camera_x % self.width)

        for x in range(start_x, screen.get_width(), self.width):
            screen.blit(self.image, (x, 0))