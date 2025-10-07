import random

from pygame import Surface, Vector2

from scripts.game.game_objects.game_object import GameObject


from scripts.game.components.animation import Animation
from scripts.game.components.animation_handler import AnimationHandler


class TestEntity(GameObject):

    def __init__(self):

        super().__init__()

        self.dim = Vector2(32, 32)

        self.animation = AnimationHandler()
        self.animation.add("idle", Animation(["idle_1", "idle_2", "idle_3", "idle_4"], repeat=True))
        self.animation.add("animation_test", Animation(["animation_test_1", "animation_test_2", "animation_test_3", "animation_test_4"], repeat=False))
        self.animation.set_current_animation("animation_test")
        self.animation.set_default_animation("idle")


    def draw(self) -> Surface | None:

        return self.animation.get_frame()


