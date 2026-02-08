from pygame import Vector2

from scripts.game.components.filters.filter import Filter

class LowPassFilter(Filter):

    def __init__(self, alpha: float, initial_value: float | Vector2):
        self.alpha = alpha
        self.filtered_value = initial_value

    def apply(self,  new_value: float | Vector2) -> float:

        self.filtered_value = (self.alpha * new_value) + (1.0 - self.alpha) * self.filtered_value

        return self.filtered_value