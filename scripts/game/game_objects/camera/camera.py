__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

from pygame import Vector2

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from scripts.services.service_locator import ServiceLocator
from scripts.game.components.time import Time
from scripts.game.game_objects.game_object import GameObject
import scripts.utility.glob as glob
glob.init()

class Camera(GameObject):

    """Class for camera used for game
    """

    def __init__(self,
            pos: Vector2 = Vector2(0, 0),
            scale: float = 1):

        super().__init__(pos = pos)
        self.scale = scale

        self.time_service: Time = ServiceLocator.get(Time)

    def adjust_scale(self, scale: float):
        new_scale = self.scale + (scale * self.time_service.elapsed_time)
        self.set_scale(new_scale)

    def set_scale(self, scale: float):
        if scale != self.scale:
            
            if scale >= 1:
                self.scale = scale
            
            else:
                self.scale = 1