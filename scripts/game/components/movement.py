from pygame import Vector2
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.time_service import TimeService
from scripts.utility.logger import Logger


class Movement:

    ## Alignment Static Variables.
    ALIGN_TOP_KW = "align_top"
    ALIGN_RIGHT_KW = "align_right"
    ALIGN_BOTTOM_KW = "align_bottom"
    ALIGN_LEFT_KW = "align_left"

    DEFAULT_ALIGN_DICT = {
        ALIGN_TOP_KW: False,
        ALIGN_RIGHT_KW: False,
        ALIGN_BOTTOM_KW: False,
        ALIGN_LEFT_KW: False}

    __ALIGNMENT_KW_DOES_NOT_EXIST = "Alignment '{align_kw}' does not exist."

    def __init__(self,
                 pos: Vector2 | None = None,
                 dim: Vector2 | None = None,
                 point_of_origin_pixel_adjustment: Vector2 | None = None,
                 **point_of_origin_alignment_kwargs: bool):

        self.__pos = Vector2(pos) if pos is not None else Vector2(0, 0)
        self.__previous_pos = Vector2(0, 0)
        self.__previous_pos = Vector2(self.__pos)

        self.__dim = Vector2(dim) if dim is not None else Vector2(0, 0)

        self.__point_of_origin_adjustment = point_of_origin_pixel_adjustment
        self.__point_of_origin_alignment = self.DEFAULT_ALIGN_DICT.copy()
        self.__pos_with_point_of_origin_adjustment = Vector2(self.__pos)
        self.set_point_of_origin_alignment(**point_of_origin_alignment_kwargs)

        self.__time_service: TimeService = ServiceLocator.get(TimeService)


    def set_point_of_origin_alignment(self,
                                      pixel_adjustment: Vector2 | None = None,
                                      **alignment_kwargs: dict[str, bool]):
        if pixel_adjustment:
            self.__point_of_origin_adjustment = pixel_adjustment

        for align_name in alignment_kwargs:
            if not Logger.raise_incorrect_type(alignment_kwargs[align_name], bool):
                if align_name in self.__point_of_origin_alignment:
                    self.__point_of_origin_alignment[align_name] = alignment_kwargs[align_name]
                else:
                    Logger.log_warning(self.__ALIGNMENT_KW_DOES_NOT_EXIST.format(align_kw=align_name))

        self.__pos_with_point_of_origin_adjustment = self.__get_pos_with_point_of_origin_adjustment(self.__pos)


    def set_dim(self, dim: Vector2):
        if self.__dim != dim:
            if not Logger.raise_incorrect_type(dim, Vector2):
                self.__dim = Vector2(dim)
                self.__pos_with_point_of_origin_adjustment = self.__get_pos_with_point_of_origin_adjustment(self.__pos)


    def get_dim(self):
        return self.__dim


    def set_pos(self, pos: Vector2) -> bool:
        """
        Sets the position of the object.

        Args:
            pos (Vector2): The new position of the object.
        """

        if pos != self.__pos:
            self.__pos = Vector2(pos)
            return True

        return False


    def get_pos(self):
        return self.__pos


    def move_pos(self, velocity: Vector2) -> bool:
        """
        Moves the position of the object. Takes into account the time elapsed since last frame.

        Args:
            velocity (Vector2): The velocity of the object.
        Returns:
            bool: True if the object moved, False otherwise.
        """

        if velocity.length_squared() > 0:
            self.__pos += velocity * self.__time_service.fixed_delta_time
            return True

        return False


    def __get_pos_with_point_of_origin_adjustment(self, pos: Vector2) -> Vector2:

        new_pos = Vector2(pos) - Vector2(self.__dim.x / 2, self.__dim.y / 2)

        if self.__point_of_origin_alignment[self.ALIGN_TOP_KW]:
            new_pos += Vector2(0, self.__dim.y / 2)

        if self.__point_of_origin_alignment[self.ALIGN_BOTTOM_KW]:
            new_pos -= Vector2(0, self.__dim.y / 2)

        if self.__point_of_origin_alignment[self.ALIGN_RIGHT_KW]:
            new_pos -= Vector2(self.__dim.x / 2, 0)

        if self.__point_of_origin_alignment[self.ALIGN_LEFT_KW]:
            new_pos += Vector2(self.__dim.x / 2, 0)

        if self.__point_of_origin_adjustment:
            new_pos += self.__point_of_origin_adjustment

        return new_pos


    def get_draw_pos(self) -> Vector2:
        """
        Returns the position to draw the object at. Takes into account interpolated time. ONLY RUN THIS METHOD ONCE PER
        FRAME PER OBJECT, as it sets the objects previous position.

        Returns:
            Vector2: The position to draw the object at.
        """
        interpolated_time = max(0.0, min(1.0, self.__time_service.interpolated_time))

        if self.__previous_pos != self.__pos:
            drawn_pos = self.__previous_pos + (self.__pos - self.__previous_pos) * interpolated_time
            self.__previous_pos = Vector2(self.__pos)

            self.__pos_with_point_of_origin_adjustment = self.__get_pos_with_point_of_origin_adjustment(self.__pos)

            return self.__get_pos_with_point_of_origin_adjustment(drawn_pos)

        else:
            return self.__pos_with_point_of_origin_adjustment



