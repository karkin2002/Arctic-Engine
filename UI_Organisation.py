import pygame

class UIElement:
    
    DEFAULT_ALIGN_DICT = {
        "align_up": False,
        "align_right": False,
        "align_down": False,
        "align_left": False}

    def __init__(self, surf_dim: tuple[int, int], dim: tuple[int, int], offset: tuple[int, int] = (0, 0), centered = True, **align_args: dict[str, bool]):
        """Constuctor for UIElement class.
        
        Sets the dimensions & position of the UIElement.

        Args:
            dim (tuple[int, int]): Dimensions as (<width>, <height>).
            pos (tuple[int, int]): Position as (<x>, <y>).
        """        
        self.dim: tuple[int, int] = dim
        self.offset: tuple[int, int] = offset
        
        self.alignment = self.DEFAULT_ALIGN_DICT
        self.__set_align(**align_args)
        self.__centered = centered
        
        self.set_pos(surf_dim)

        
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
            
        pygame.draw.rect(surf, (255, 0, 0), (self.__pos, self.dim))
        
        
    def set_pos(self, surf_dim: tuple[int, int]):
        
        self.__pos = [0, 0]
        for i in range(2):
            
            half_surf_len = round(surf_dim[i] / 2)
            
            offset = self.offset[i]
            
            if i == 0 and not (self.alignment["align_right"] and self.alignment["align_left"]):
                
                if self.alignment["align_right"]:
                    offset += half_surf_len
                
                elif self.alignment["align_left"]:
                    offset -= half_surf_len
                    
            if i == 1 and not (self.alignment["align_up"] and self.alignment["align_down"]):
                
                if self.alignment["align_down"]:
                    offset += half_surf_len
                
                elif self.alignment["align_up"]:
                    offset -= half_surf_len
        
            if self.__centered:
                offset -= round(self.dim[i] / 2)
            
            self.__pos[i] = half_surf_len + offset
                    





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
        self.resized: bool = False
        
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
        
        self.resized = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
            
        if self.resized:
            self.resize()
                
        return True
    
    
    def draw(self):
        """Draws the UI to the window.
        """
        
        window.win.fill((255, 255, 255))
        
        self.__draw_elems()

        pygame.display.flip()

        self.__clock.tick(60)
        
        
    def resize(self):
        self.win_dim = (self.win.get_width(), self.win.get_height())
        self.__resize_elems()
        
    
    def add_elem(self, elem_name: str, dim: tuple[int, int], offset: tuple[int, int] = (0, 0), **align_args):
        self.__ui_elems[elem_name] = UIElement(self.win_dim, dim, offset, **align_args)
    
        
    def __draw_elems(self):
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].draw(self.win)
            
    def __resize_elems(self):
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].set_pos(self.win_dim)
        
        
        
        



pygame.init()

window = UI()

window.add_elem("test 1", (100, 100))

run = True

while run:

    if not window.events():
        run = False

    window.draw()


pygame.quit()