import pygame

class UIElement:
    
    DEFAULT_ALIGN_DICT = {
        "align_up": False,
        "align_right": False,
        "align_down": False,
        "align_left": False}

    def __init__(self, surf_dim: tuple[int, int], dim: tuple[int, int], offset: tuple[int, int] = (0, 0), centered = True, **align_args: dict[str, bool]):
        """_summary_

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of surf to be drawn 
            on.
            dim (tuple[int, int]): Dimensions as (<width>, <height>).
            offset (tuple[int, int], optional): Offset in pixels from it's 
            original alignment. Defaults to (0, 0).
            centered (bool, optional): Whether the element should be drawn from 
            the center of its width/height. Defaults to True.
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_up=<bool>, 
            align_right=<bool>, align_down=<bool>, align_left=<bool>.
        """      
          
        self.dim: tuple[int, int] = dim
        self.offset: tuple[int, int] = offset
        
        self.alignment = self.DEFAULT_ALIGN_DICT
        self.__set_align(**align_args)
        self.__centered = centered
        
        self.set_pos(surf_dim)

        
    def __set_align(self, **align_args: dict[str, bool]):
        """Sets the alignment for the UI Element.

        Args:
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_up=<bool>, 
            align_right=<bool>, align_down=<bool>, align_left=<bool>.
        """        
        
        for align_name in align_args:
            if type(align_args[align_name]) == bool: 
                if align_name in self.alignment:
                    self.alignment[align_name] = align_args[align_name]
            else:
                raise AttributeError(f"Alignment argument is of type '{type(align_args[align_name])}'. However, this needs to be of type 'bool'.")
        
        
    def draw(self, surf: pygame.Surface):
        """Draws the UIElement on a surface.

        Args:
            surf (Surface): Surface to be drawn on.
        """   
            
        pygame.draw.rect(surf, (255, 0, 0), (self.__pos, self.dim))
        
        
    def set_pos(self, surf_dim: tuple[int, int]):
        """Sets the position for the UI Element to be displayed on a surface.

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
        """        
        
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
            win_dim (tuple[int, int], optional): Window (<width>, <height>). Defaults to (700, 500).
        """        
        
        self.win_dim: tuple[int, int] = None
        self.win: pygame.Surface = None

        self.__clock = pygame.time.Clock()
        
        self.__set_win(win_dim)
        self.resized: bool = False
        
        self.__ui_elems: dict[str, UIElement] = {}


    def __set_win(self, win_dim: tuple[int, int]):
        """Creates a new window.

        Args:
            win_dim (tuple[int, int]): Window (<width>, <height>).
        """        

        self.win_dim = win_dim
        self.win = pygame.display.set_mode(self.win_dim, pygame.RESIZABLE)


    def events(self) -> bool:
        """Handles the windows events; including handeling resizing & quitting.

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
            self.__resize()
                
        return True
    
    
    def draw(self):
        """Draws a new frame of the window; including all its elements.
        """
        
        window.win.fill((255, 255, 255))
        
        self.__draw_elems()

        pygame.display.flip()

        self.__clock.tick(60)
        
        
    def __resize(self):
        """Resizes the window, updating all its elements.
        """        
        
        self.win_dim = (self.win.get_width(), self.win.get_height())
        self.__resize_elems()
        
    
    def add_elem(self, elem_name: str, dim: tuple[int, int], offset: tuple[int, int] = (0, 0), **align_args: dict[str, bool]):
        """Adds a UI Element to be displayed on the window.

        Args:
            elem_name (str): Arbitrary name.
            dim (tuple[int, int]): Dimensions of the UI Element.
            offset (tuple[int, int], optional): Offset in pixels from it's 
            original alignment. Defaults to (0, 0).
            align_args (dict[str, bool], optional): Specify which side of the
            window the UI Element should align to. Options are align_up=<bool>, 
            align_right=<bool>, align_down=<bool>, align_left=<bool>.
        """        
        
        self.__ui_elems[elem_name] = UIElement(self.win_dim, dim, offset, **align_args)
    
        
    def __draw_elems(self):
        """Draws UI elements on the window.
        """        
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].draw(self.win)
            
            
    def __resize_elems(self):
        """Resizes UI Elements based on the window dimensions.
        """ 
              
        for elem_name in self.__ui_elems:
            self.__ui_elems[elem_name].set_pos(self.win_dim)
        
        


pygame.init()

window = UI()

window.add_elem("Test Element 1", (100, 100))

run = True

while run:

    if not window.events():
        run = False

    window.draw()

pygame.quit()