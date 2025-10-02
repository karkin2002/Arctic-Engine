from pygame import Vector2
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.time_service import Time

class Movement:

    def __init__(self,
                 pos: Vector2 | None = None):

        self.pos = Vector2(pos) if pos is not None else Vector2(0, 0)
        self.previous_pos = Vector2(0, 0)
        self.previous_pos.update(self.pos)

        self.time_service: Time = ServiceLocator.get(Time)


    def set_pos(self, pos: Vector2) -> bool:
        """
        Sets the position of the object.

        Args:
            pos (Vector2): The new position of the object.
        """

        if pos != self.pos:
            self.pos = Vector2(pos)
            return True

        return False


    def move_pos(self, velocity: Vector2) -> bool:
        """
        Moves the position of the object. Takes into account the time elapsed since last frame.

        Args:
            velocity (Vector2): The velocity of the object.
        Returns:
            bool: True if the object moved, False otherwise.
        """

        if velocity.length_squared() > 0:
            self.pos += velocity * self.time_service.fixed_delta_time
            return True

        return False


    def get_draw_pos(self) -> Vector2:
        """
        Returns the position to draw the object at. Takes into account interpolated time. ONLY RUN THIS METHOD ONCE PER
        FRAME PER OBJECT, as it sets the objects previous position.

        Returns:
            Vector2: The position to draw the object at.
        """
        interpolated_time = max(0.0, min(1.0, self.time_service.interpolated_time))

        if self.previous_pos != self.pos:
            drawn_pos = self.previous_pos + (self.pos - self.previous_pos) * interpolated_time
            self.previous_pos = Vector2(self.pos)

            return drawn_pos

        else:
            return self.pos



