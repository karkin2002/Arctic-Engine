__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

import pygame

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from scripts.services.service_locator import ServiceLocator
from scripts.game.time import Time
from scripts.game.components.component import Component
import scripts.utility.glob as glob
glob.init()

class Camera(Component):

    """Class for camera used for game
    """

    def __init__(self,
            pos: tuple = (0, 0),
            scale: float = 1):

        super().__init__(pos = list(pos))
        self.scale = scale
        self.camera_scale_changed = False
        self.camera_pos_changed = False

        self.time_service: Time = ServiceLocator.get(Time)
        

    def move_pos(self, values: tuple[float, float]):
        if values[0] != 0 or values[1] != 0:
            self.pos[0] += values[0] * self.time_service.elapsed_time
            self.pos[1] += values[1] * self.time_service.elapsed_time
            self.camera_pos_changed = True
    

    def set_pos(self, pos: tuple[int, int]):
        if pos != self.pos:
            self.pos = list(pos)
            self.camera_pos_changed = True
        

    def adjust_scale(self, scale: float):
        new_scale = self.scale + (scale * self.time_service.elapsed_time)
        self.set_scale(new_scale)


    def set_scale(self, scale: float):
        if scale != self.scale:
            
            if scale >= 1:
                self.scale = scale
            
            else:
                self.scale = 1
            
            self.camera_scale_changed = True