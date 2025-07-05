class Component:

    __DEFAULT_IDENT = "Component-{comp_num}"

    comp_num = 0

    def __init__(self,
                 ident: str = __DEFAULT_IDENT.format(comp_num = comp_num),
                 coord: list[int] = [0, 0]):

        self.ident = ident
        self.coord = coord


    def draw(self):
        """
        Draws the component. By default, this method has no implementation.
        """
        pass

    def update(self):
        """
        Updates the component every frame. By default, this method has no implementation.
        """
        pass

    def fixed_update(self):
        """
        Updates the component by a fixed value. By default, this method has no implementation.
        """
        pass