from abc import ABC, abstractmethod
import time

class Weapon(ABC):
    def __init__(self, damage, fire_rate, bullet_speed):
        self._damage = damage
        self._fire_rate = fire_rate
        self._bullet_speed = bullet_speed
        self._last_shot = 0

    def can_shoot(self):
        current = time.time()
        return current - self._last_shot >= self._fire_rate

    @abstractmethod
    def shoot(self, owner, bullets, target_pos=None):
        pass