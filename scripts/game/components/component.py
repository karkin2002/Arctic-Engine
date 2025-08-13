from pygame import Surface

class Component:

    __DEFAULT_IDENT = "Component-{comp_num}"

    comp_num = 0

    def __init__(self,
                 ident: str = __DEFAULT_IDENT.format(comp_num = comp_num),
                 pos: list[int] = [0, 0],
                 dim: tuple[int, int] = (0, 0)):

        self.ident = ident
        self.pos = pos
        self.dim = dim

    def draw(self) -> Surface | None:
        """
        Draws the component. By default, this method has no implementation.
        """
        pass

    def update(self):
        """
        Updates the component every frame. By default, this method has no implementation.
        """
        pass