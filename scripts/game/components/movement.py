from enum import Enum
from pygame import Vector2
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.time_service import TimeService

class PointOfOrigin(Enum):
    CENTER = "CENTER"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    TOP = "TOP"
    BOTTOM = "BOTTOM"

class Movement:

    def __init__(self,
                 pos: Vector2 | None = None,
                 dim: Vector2 | None = None,
                 point_of_origin_alignment: PointOfOrigin | None = None,
                 point_of_origin_adjustment: Vector2 | None = None):

        self.pos = Vector2(pos) if pos is not None else Vector2(0, 0)
        self.previous_pos = Vector2(0, 0)
        self.previous_pos = Vector2(self.pos)

        self.dim = Vector2(dim) if dim is not None else Vector2(0, 0)

        self.point_of_origin_alignment = point_of_origin_alignment
        self.point_of_origin_adjustment = point_of_origin_adjustment

        self.__time_service: TimeService = ServiceLocator.get(TimeService)


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
            self.pos += velocity * self.__time_service.fixed_delta_time
            return True

        return False


    def __get_point_of_origin(self, pos: Vector2) -> Vector2:

        if self.point_of_origin_alignment == PointOfOrigin.CENTER:
            return pos - Vector2(self.dim.x / 2, self.dim.y / 2)

        return pos


    def get_draw_pos(self) -> Vector2:
        """
        Returns the position to draw the object at. Takes into account interpolated time. ONLY RUN THIS METHOD ONCE PER
        FRAME PER OBJECT, as it sets the objects previous position.

        Returns:
            Vector2: The position to draw the object at.
        """
        interpolated_time = max(0.0, min(1.0, self.__time_service.interpolated_time))

        if self.previous_pos != self.pos:
            drawn_pos = self.previous_pos + (self.pos - self.previous_pos) * interpolated_time
            self.previous_pos = Vector2(self.pos)

            return self.__get_point_of_origin(drawn_pos)

        else:
            return self.__get_point_of_origin(self.pos)



