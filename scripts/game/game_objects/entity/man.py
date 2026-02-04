from pygame import Surface, Vector2
from scripts.game.game_objects.game_object import GameObject
from scripts.services.service_locator import ServiceLocator
from scripts.services.visual.image_service import ImageService


class Man(GameObject):

    def __init__(self):

        super().__init__()

        self.move.set_dim(Vector2(32, 32))

        self.image_name = "down1"

        self.__image_service: ImageService = ServiceLocator.get(ImageService)


    def draw(self) -> Surface | None:

        return self.__image_service.get(self.image_name).surface


