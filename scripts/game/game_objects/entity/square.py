from pygame import Surface, Vector2
from scripts.game.game_objects.game_object import GameObject
from scripts.services.service_locator import ServiceLocator
from scripts.services.visual.image_service import ImageService


class Square(GameObject):

    TEXTURE_NAME = "square"

    def __init__(self):

        super().__init__()

        self.__image_service: ImageService = ServiceLocator.get(ImageService)

        self.move.set_dim(Vector2(self.__image_service.get(Square.TEXTURE_NAME).dim))


    def draw(self) -> Surface | None:
        return self.__image_service.get(Square.TEXTURE_NAME).surface


