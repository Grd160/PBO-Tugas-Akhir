import math
import time
from Weapon.Weapon import Weapon
from Object.Bullet import Bullet
from Setting import ORANGE

class RapidWeapon(Weapon):
    def __init__(self):
        super().__init__(damage=10, fire_rate=0.1, bullet_speed=14)

    def shoot(self, owner, bullets, target_pos=None):
        if not self.can_shoot():
            return

        self._last_shot = time.time()

        mx, my = target_pos

        ox = owner.get_rect().centerx
        oy = owner.get_rect().centery

        angle = math.atan2(my - oy, mx - ox)

        dx = math.cos(angle) * self._bullet_speed
        dy = math.sin(angle) * self._bullet_speed

        bullets.append(Bullet(ox, oy, dx, dy, self._damage, owner, ORANGE))