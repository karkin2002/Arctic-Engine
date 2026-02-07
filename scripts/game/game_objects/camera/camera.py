__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from pygame import Vector2
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.time_service import TimeService
from scripts.game.game_objects.game_object import GameObject
from scripts.utility.math.LowPassFilter import LowPassFilter

class Camera(GameObject):

    """Class for camera used for game
    """

    __LOW_PASS_FILTER_ALPHA = 0.1

    def __init__(self,
            pos: Vector2 = Vector2(0, 0),
            scale: float = 1):

        super().__init__(pos = pos, display=False)

        ## The implementation for scale is currently not implemented. The general structure for it is in place, but it's
        ## full implementation was never fleshed out.
        ##
        ## Idea: Camera obj stores a scale value. gameObjects scale based on the camera's scale value. When the scale
        ## changes or new object comes into view, we can cache their scaled up surface (caching could be preformed on a
        ## separate thread to reduce workload). This would additionally require chunking the map, so that only visible
        ## segments would be loaded / visible.
        ##
        ## This feature will be revisited at a later date, for now I will work on something else...
        self.scale = scale

        self.time_service: TimeService = ServiceLocator.get(TimeService)

    def world_to_screen(self, world_pos: Vector2, window_center: Vector2):

        relative = (world_pos - self.move.get_pos()) * self.scale

        return window_center + relative

    def adjust_scale(self, scale: float):
        new_scale = self.scale + (scale * self.time_service.elapsed_time)
        self.set_scale(new_scale)

    def set_scale(self, scale: float):
        if scale != self.scale:
            
            if scale >= 1:
                self.scale = scale
            
            else:
                self.scale = 1.0