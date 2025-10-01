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

from scripts.services.service_locator import ServiceLocator
from scripts.services.image_service import ImageService, Image


class Tile:

    def __init__(self, 
                 dim: tuple[int, int]):
        
        self.dim = dim



class DynamicTile(Tile):
    
    def __init__(self):
        super().__init__((100,100))
    
    
    
class StaticTile(Tile):

    def __init__(self, 
                 texture_img_name: str):
        
        self.texture_img_name = texture_img_name
        self.__time_service_locator = ServiceLocator().get(ImageService)
        
        super().__init__(
            self.__time_service_locator.get_image(self.texture_img_name).dim
        )
        
    def get_texture_surf(self):
        return self.__time_service_locator.get_image(self.texture_img_name).surface