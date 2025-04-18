# world/entities/object.py
import random
import uuid
from world.config import ENERGY_GAIN_PER_FOOD


class WorldObject:
    def __init__(self, obj_type: str, weight: float = 1.0, stackable: bool = True):
        self.id = uuid.uuid4()
        self.type = obj_type
        self.weight = weight
        self.stackable = stackable

    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type} weight={self.weight}>"


# === Заглушки объектов ===

class Food(WorldObject):
    def __init__(self, nutrition=ENERGY_GAIN_PER_FOOD, amount=1, decay=None, stackable=True):
        super().__init__("food", weight=0.5 * amount, stackable=stackable)
        self.nutrition_per_unit = nutrition
        self.amount = amount
        self.decay = decay  # None = не портится

    def take_bite(self, bite_size=1):
        eaten = min(bite_size, self.amount)
        self.amount -= eaten
        return eaten * self.nutrition_per_unit

    def is_empty(self):
        return self.amount <= 0

    def tick_decay(self):
        if self.decay is not None:
            self.decay -= 1
            return self.decay <= 0  # True → испортилось
        return False

    def __repr__(self):
        return f"<Food amt={self.amount} decay={self.decay}>"


class Stick(WorldObject):
    def __init__(self, size=1.0, amount=1):
        super().__init__("stick", weight=size, stackable=True)
        self.amount = amount

    def add_one(self):
        self.amount += 1
        return self.amount >= 3  # True, если надо преобразовать

    def is_barricade(self):
        return self.amount >= 3

    def remove_one(self):
        self.amount -= 1
        return self.amount <= 0

class Barricade(WorldObject):
    def __init__(self):
        super().__init__("barricade", weight=9999)  # или неважно
        self.blocks_movement = True

class Corpse(Food):
    def __init__(self, size=1.0):
        amount = int(3 + size * 5)
        nutrition = 25  # на 1 "единицу"
        super().__init__(nutrition=nutrition, amount=amount, decay=80, stackable=True)
        self.type = "corpse"
        self.weight = size

    def remove_one(self):
        self.amount -= 1
        return self.amount <= 0

class Berry(Food):
    def __init__(self):
        decay = random.randint(30, 60)
        super().__init__(nutrition=10, amount=1, decay=decay, stackable=True)
        self.type = "berry"

    def remove_one(self):
        self.amount -= 1
        return self.amount <= 0
