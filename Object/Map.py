from Object.Platform import Platform
from Object.Box import Box
from Char.Enemy import Enemy

class GameMap:
    def __init__(self):
        self.platforms = [
            Platform(0, 650, 5000, 70),
            Platform(400, 540, 300, 30),
            Platform(1000, 540, 300, 30),
            Platform(1800, 540, 300, 30),
            Platform(2500, 540, 300, 30)
        ]

        self.boxes = [
            Box(700, 600),
            Box(1600, 600),
            Box(2400, 600)
        ]

        self.enemies = [
            Enemy(900, 580),
            Enemy(1400, 580),
            Enemy(2000, 580),
            Enemy(2700, 580),
            Enemy(3300, 580)
        ]