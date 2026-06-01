from Object.Platform import Platform
from Object.Box import Box
from Char.Enemy import Enemy
from Char.Boss import Boss

class Stage2:
    name = "Stage 2 - Forest"
    description = "Medan lebih tinggi, musuh lebih banyak"

    @staticmethod
    def create_map():
        # Platform lantai dasar dan platform melayang untuk manuver
        platforms = [
            Platform(0, 650, 5000, 70),
            Platform(300, 500, 200, 20),
            Platform(700, 400, 200, 20),
            Platform(1200, 450, 300, 30),
            Platform(2000, 500, 250, 20),
        ]

        # Penempatan box sebagai rintangan
        boxes = [
            Box(500, 600),
            Box(1500, 600),
            Box(2500, 600),
        ]

        # Penempatan musuh di posisi yang lebih bervariasi
        enemies = [
            Enemy(600, 580),
            Enemy(1100, 580),
            Enemy(1600, 580),
            Enemy(2200, 580),
            Enemy(2800, 580),
            Enemy(3500, 580),
        ]

        # Bos diletakkan di bagian akhir map
        boss = Boss(4500, 120)

        return platforms, boxes, enemies, boss