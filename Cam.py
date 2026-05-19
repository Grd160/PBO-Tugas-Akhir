from Setting import WIDTH, MAP_WIDTH

class Camera:
    def __init__(self):
        self.x = 0

    def update(self, target):
        target_x = target.get_rect().centerx - WIDTH // 2

        self.x += (target_x - self.x) * 0.08

        if self.x < 0:
            self.x = 0

        if self.x > MAP_WIDTH - WIDTH:
            self.x = MAP_WIDTH - WIDTH