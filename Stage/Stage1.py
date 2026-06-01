from Object.Platform import Platform
from Object.Box import Box
from Char.Enemy import Enemy
from Char.Boss import Boss
 
class Stage1:
    name = "Stage 1 - Wasteland"
    description = "Stage berisi 5 musuh dan 1 Boss"
 
    @staticmethod
    def create_map():
        platforms = [
            Platform(0, 650, 5000, 70),
            Platform(400, 540, 300, 30),
            Platform(1000, 540, 300, 30),
            Platform(1800, 540, 300, 30),
            Platform(2500, 540, 300, 30),
        ]
 
        boxes = [
            Box(700, 600),
            Box(1600, 600),
            Box(2400, 600),
        ]
 
        enemies = [
            Enemy(900, 580),
            Enemy(1400, 580),
            Enemy(2000, 580),
            Enemy(2700, 580),
            Enemy(3300, 580),
        ]
 
        boss = Boss(4300, 120)
 
        return platforms, boxes, enemies, boss