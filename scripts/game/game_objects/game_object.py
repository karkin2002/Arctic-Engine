from pygame import Surface, Vector2
from scripts.game.components.movement import Movement

class GameObject:

    __DEFAULT_IDENT = "GameObject-{comp_num}"

    comp_num = 0

    def __init__(self,
                 ident: str = __DEFAULT_IDENT.format(comp_num = comp_num),
                 pos: Vector2 = Vector2(0, 0),
                 dim: Vector2 = Vector2(0, 0)):

        self.ident = ident
        self.move = Movement(pos)
        self.dim = dim

    def update(self):
        """
        Updates the game object every frame. By default, this method has no implementation.
        """
        pass

    def draw(self) -> Surface | None:
        """
        Draws the game object. By default, this method has no implementation.
        """
        pass