from pygame import Surface, Vector2
from scripts.game.game_objects.game_object import GameObject
from scripts.game.components.animation import Animation
from scripts.game.components.animation_handler import AnimationHandler


class TestEntity(GameObject):

    def __init__(self):

        super().__init__()

        self.move.set_dim(Vector2(32, 32))

        self.animation = AnimationHandler()
        self.animation.add("idle", Animation(["idle_1", "idle_2", "idle_3", "idle_4", "idle_5", "idle_6", "idle_7", "idle_8", "idle_9", "idle_10", "idle_11", "idle_12"]))
        self.animation.add("right", Animation(["right_1", "right_2", "right_3", "right_4", "right_5", "right_6", "right_7", "right_8", "right_9", "right_10", "right_11", "right_12"]))
        self.animation.add("left", Animation(["left_1", "left_2", "left_3", "left_4", "left_5", "left_6", "left_7", "left_8", "left_9", "left_10", "left_11", "left_12"]))
        self.animation.add("up", Animation(["up_1", "up_2", "up_3", "up_4", "up_5", "up_6", "up_7", "up_8", "up_9", "up_10", "up_11", "up_12"]))
        self.animation.add("down", Animation(["down_1", "down_2", "down_3", "down_4", "down_5", "down_6", "down_7", "down_8", "down_9", "down_10", "down_11", "down_12"]))
        self.animation.add("animation_test", Animation(["animation_test_1", "animation_test_2", "animation_test_3", "animation_test_4"], repeat=False))
        self.animation.set_default_animation("idle")


    def draw(self) -> Surface | None:

        return self.animation.get_frame()


