import pygame
from pygame import font as pyfont
from logger import Logger
import globvar
globvar.init()

def check_is_pair(value: tuple | list) -> tuple | list:
    """Returns the value inputted, if it's a tuple or list with a len of 2.
    Otherwise raises an error.

    Args:
        value (tuple | list | any): Value to check.

    Raises:
        AttributeError: Value isn't a tuple or list of len 2.

    Returns:
        tuple: The input value.
    """    
    
    if type(value) == tuple or type(value) == list and len(value) == 2:
        return value
    
    else:
        Logger.raise_incorrect_type(value, tuple | list)
        
        

## Returns a surface to display text
def createText(text: str, font: str, colour: tuple, size: int) -> pygame.Surface:
    """Creates a surface with text on it.

    Args:
        text (str): Text to be drawn on the surface.
        font (str): Font of the text.
        colour (tuple): Colour of the text.
        size (int): Size of the text.

    Returns:
        pygame.Surface: Surface with text.
    """

    if font in pyfont.get_fonts():
        fontFormat = pyfont.SysFont(font, size)
    else:
        fontFormat = pyfont.Font(str(font), size)

    message = fontFormat.render(text, True, colour)

    return message



## UI Element Class
class UIElement:
    
    ## Alignment Static Variables.
    ALIGN_UP_KW = "align_up"
    ALIGN_RIGHT_KW = "align_right"
    ALIGN_DOWN_KW = "align_down"
    ALIGN_LEFT_KW = "align_left"
    
    DEFAULT_ALIGN_DICT = {
        ALIGN_UP_KW: False,
        ALIGN_RIGHT_KW: False,
        ALIGN_DOWN_KW: False,
        ALIGN_LEFT_KW: False}

    def __init__(self, 
                 surf_dim: tuple[int, int], 
                 dim: tuple[int, int], 
                 offset: tuple[int, int] = (0, 0), 
                 alpha: int = 255,
                 centered: bool = True, 
                 display: bool = True,
                 **align_args: dict[str, bool]):
        
        """Constuctor for UIElement class.

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
        self.alignment = self.DEFAULT_ALIGN_DICT.copy()
            
        self.__set_align(**align_args)
        self.__centered = centered
        
        self.set_pos(surf_dim)
        
        self.__alpha = alpha
        self.__display = display
        
        self.__surf = None
        
    def __set_align(self, **align_args: dict[str, bool]):
        """Sets the alignment for the UI Element.

        Args:
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_up=<bool>, 
            align_right=<bool>, align_down=<bool>, align_left=<bool>.
        """        
        
        for align_name in align_args:
            if not Logger.raise_incorrect_type(align_args[align_name], bool):
                if align_name in self.alignment:
                    self.alignment[align_name] = align_args[align_name]          
                
                
    def set_surf(self, surf_dim: tuple[int, int], surf: pygame.Surface):
        """Sets the UI Elements surface. 

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
            surf (Surface): The surface to be set.
        """        
        
        self.__surf = surf
        self.dim = (surf.get_width(), surf.get_height())
        self.set_pos(surf_dim)
        
        
        
    def draw(self, surf: pygame.Surface):
        """Draws the UIElement on a surface.

        Args:
            surf (Surface): Surface to be drawn on.
        """   
            
        if self.__is_displayed():
            surf.blit(self.__surf, self.__pos)
            
            
    def __is_displayed(self) -> bool:
        """Returns whether the UIElement is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """        
        return self.__display and self.__alpha > 0 and self.__surf != None
        
        
        
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
            
            if i == 0 and not (self.alignment[self.ALIGN_RIGHT_KW] and self.alignment[self.ALIGN_LEFT_KW]):
                
                if self.alignment[self.ALIGN_RIGHT_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_LEFT_KW]:
                    offset -= half_surf_len
                    
            if i == 1 and not (self.alignment[self.ALIGN_UP_KW] and self.alignment[self.ALIGN_DOWN_KW]):
                
                if self.alignment[self.ALIGN_DOWN_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_UP_KW]:
                    offset -= half_surf_len
        
            if self.__centered:
                offset -= round(self.dim[i] / 2)
            
            self.__pos[i] = half_surf_len + offset
                    


class Text(UIElement):
    
    def __init__(self, 
                 surf_dim: tuple[int, int], 
                 text: str,
                 size: str,
                 font: str,
                 colour: str,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 **align_args: dict[str, bool]):
        
        super().__init__(
            surf_dim,
            (100, 100),
            offset,
            alpha,
            centered,
            display,
            **align_args
        )
        
        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        
        self.__create_text_surf(surf_dim)
        
        
    def update_text(self, 
                    surf_dim: tuple[int, int],
                    text: str = None, 
                    font: str = None, 
                    colour: str = None, 
                    size: int = None):
        
        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        
        self.__create_text_surf(surf_dim)
        
        
    def __create_text_surf(self, surf_dim):
            
        self.set_surf(
            surf_dim, 
            createText(
                self.text,
                self.font, 
                globvar.get_colour(self.colour), 
                self.size))






