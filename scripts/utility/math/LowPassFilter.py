class LowPassFilter:

    def __init__(self, alpha: float, initial_value: float = 0.0):
        self.alpha = alpha
        self.filtered_value = initial_value

    def update_filter(self,  new_value: float) -> float:

        self.filtered_value = (self.alpha * new_value) + (1.0 - self.alpha) * self.filtered_value

        return self.filtered_value
