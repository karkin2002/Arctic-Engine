from pygame import Surface, Vector2
from scripts.game.components.movement import Movement
from scripts.game.components.tag_handler import TagHandler
from scripts.services.visual.colour_service import ColourService


class GameObject:

    __DEFAULT_IDENT = "GameObject-{comp_num}"

    comp_num = 0

    __default_surface = Surface((20, 20))
    __default_surface.fill(ColourService.ERROR_COLOUR_VALUE)

    def __init__(self,
                 ident: str = __DEFAULT_IDENT.format(comp_num = comp_num),
                 pos: Vector2 | None = None,
                 dim: Vector2 | None = None,
                 display: bool = True):

        self.ident = ident
        self.move = Movement(pos, dim)
        self.display = display
        self.tag = TagHandler()

        GameObject.comp_num += 1

    def update(self):
        """
        Updates the game object every frame. By default, this method has no implementation.
        """
        pass

    def draw(self) -> Surface | None:
        """
        Draws the game object. By default, this method has no implementation.
        """
        return self.__default_surface