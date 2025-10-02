import random

from pygame import Surface

from scripts.game.game_objects.game_object import GameObject


class TestEntity(GameObject):

    def __init__(self):

        super().__init__()

        self.dim = (100, 100)
        self.entity_surf = Surface(self.dim)
        self.entity_surf.fill((
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)))


    def draw(self) -> Surface | None:

        return self.entity_surf


