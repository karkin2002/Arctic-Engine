import pygame

class UIElement:
    
    DEFAULT_ALIGN_DICT = {
        "align_up": False,
        "align_right": False,
        "align_down": False,
        "align_left": False}

    def __init__(self, dim: tuple[int, int], pos: tuple[int, int], **align_args: dict[str, bool]):
        """Constuctor for UIElement class.
        
        Sets the dimensions & position of the UIElement.

        Args:
            dim (tuple[int, int]): Dimensions as (<width>, <height>).
            pos (tuple[int, int]): Position as (<x>, <y>).
        """        
        self.dim: tuple[int, int] = dim
        self.pos: tuple[int, int] = pos
        
        self.alignment = self.DEFAULT_ALIGN_DICT
        self.__set_align(**align_args)
        pass
        
    def __set_align(self, **align_args: dict[str, bool]):
        
        for align_name in align_args:
            if type(align_args[align_name]) == bool: 
                if align_name in self.alignment:
                    self.alignment[align_name] = align_args[align_name]
            else:
                raise(f"Alignment argument is type '{type(align_args[align_name])}'. Needs to be type bool.")
        
        
    def draw(self, surf: pygame.Surface):
        """Draws the UIElement on a surface.

        Args:
            surf (Surface): Surface to draw on.
        """        
        pygame.draw.rect(surf, (255, 0, 0), (self.dim, self.pos))





class UI:
    """Class for handeling the window and its UI
    """    
    
    
    def __init__(self, win_dim: tuple[int, int] = (700, 500)):
        """Constructor for UI class

        Args:
            win_dim (tuple[int, int], optional): Window h/w. Defaults to (700, 500).
        """        
        
        self.win_dim: tuple[int, int] = None
        self.win: pygame.Surface = None

        self.__clock = pygame.time.Clock()
        
        self.__set_win(win_dim)
        
        self.__ui_elems: dict[str, UIElement] = {}


    def __set_win(self, win_dim: tuple[int, int]):
        """Sets the window to a specified h/w.

        Args:
            win_dim (tuple[int, int]): Window h/w.
        """        

        self.win_dim = win_dim
        self.win = pygame.display.set_mode(self.win_dim, pygame.RESIZABLE)


    def events(self) -> bool:
        """Handles the windows events.

        Returns:
            bool: Whether the window is open.
        """        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        return True
    
    
    def draw(self):
        """Draws the UI to the window.
        """
        
        window.win.fill((255, 255, 255))
        
        self.__draw_ui_elems()

        pygame.display.flip()

        self.__clock.tick(60)
        
    
    def add_ui_elem(self, elem_name: str, dim: tuple[int, int], offset: tuple[int, int], **align_args):
        self.__ui_elems[elem_name] = UIElement(dim, offset, **align_args)
        
    def __draw_ui_elems(self):
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].draw(self.win)
        
        
        



pygame.init()

window = UI()

window.add_ui_elem("test 1", (100, 100), (100, 100), align_up = True)

run = True

while run:

    if not window.events():
        run = False

    window.draw()


pygame.quit()