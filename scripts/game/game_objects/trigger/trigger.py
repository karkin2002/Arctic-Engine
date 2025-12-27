from pygame import Vector2, Surface
from scripts.game.game_objects.game_object import GameObject
from scripts.services.visual.colour_service import ColourService
from scripts.utility.logger import Logger


class Trigger(GameObject):

    __TRIGGER_DISPLAY_WARN = ("Trigger {trigger} has display set to True. Display for Triggers should only be used "
                              "during development & testing. It is not recommend for production for performance reasons.")

    def __init__(self,
                 pos: Vector2 = None,
                 dim: Vector2 = Vector2(32, 32),
                 display: bool = False):

        super().__init__(pos = pos, dim = dim, display = display)

        if self.display:
            Logger.log_warning(self.__TRIGGER_DISPLAY_WARN.format(trigger = self))

    def draw(self) -> Surface | None:
        __trigger_surface = Surface(self.move.get_dim())
        __trigger_surface.fill(ColourService.OUTLINE_COLOUR_VALUE)
        return __trigger_surface