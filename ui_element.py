import pygame
from pygame import font as pyfont
from logger import Logger
import globvar
globvar.init()


## UI Element Class
class UIElement:
    
    ## Alignment Static Variables.
    ALIGN_TOP_KW = "align_top"
    ALIGN_RIGHT_KW = "align_right"
    ALIGN_BOTTOM_KW = "align_bottom"
    ALIGN_LEFT_KW = "align_left"
    
    DEFAULT_ALIGN_DICT = {
        ALIGN_TOP_KW: False,
        ALIGN_RIGHT_KW: False,
        ALIGN_BOTTOM_KW: False,
        ALIGN_LEFT_KW: False}
    
    DEFAULT_DIM = (100, 100)

    def __init__(self, 
                 dim: tuple[int, int], 
                 offset: tuple[int, int] = (0, 0), 
                 alpha: int = 255,
                 centered: bool = True, 
                 display: bool = True,
                 **align_args: dict[str, bool]):
        
        """Constuctor for UIElement class.

        Args:
            dim (tuple[int, int]): Dimensions as (<width>, <height>).
            offset (tuple[int, int], optional): Offset in pixels from it's 
            original alignment. Defaults to (0, 0).
            centered (bool, optional): Whether the element should be drawn from 
            the center of its width/height. Defaults to True.
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_top=<bool>, 
            align_right=<bool>, align_bottom=<bool>, align_left=<bool>.
        """      
          
        self.dim: tuple[int, int] = dim
        self.offset: tuple[int, int] = offset
        self.alignment = self.DEFAULT_ALIGN_DICT.copy()
            
        self.__set_align(**align_args)
        self.__centered = centered
        
        self.__pos = [0, 0]
        
        self.__alpha = alpha
        self.__display = display
        
        self.__surf = None
        
    def __set_align(self, **align_args: dict[str, bool]):
        """Sets the alignment for the UI Element.

        Args:
            align_args (dict[str, bool], optional): Specifies which side of the
            surface the UI Element should align to. Options are align_top=<bool>, 
            align_right=<bool>, align_bottom=<bool>, align_left=<bool>.
        """        
        
        for align_name in align_args:
            if not Logger.raise_incorrect_type(align_args[align_name], bool):
                if align_name in self.alignment:
                    self.alignment[align_name] = align_args[align_name]          
                
                
    def _create_surf(self, surf_dim: tuple[int, int], surf: pygame.Surface):
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
        
        for i in range(2):
            
            half_surf_len = round(surf_dim[i] / 2)
            
            offset = self.offset[i]
            
            if i == 0 and not (self.alignment[self.ALIGN_RIGHT_KW] and self.alignment[self.ALIGN_LEFT_KW]):
                
                if self.alignment[self.ALIGN_RIGHT_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_LEFT_KW]:
                    offset -= half_surf_len
                    
            if i == 1 and not (self.alignment[self.ALIGN_TOP_KW] and self.alignment[self.ALIGN_BOTTOM_KW]):
                
                if self.alignment[self.ALIGN_BOTTOM_KW]:
                    offset += half_surf_len
                
                elif self.alignment[self.ALIGN_TOP_KW]:
                    offset -= half_surf_len
        
            if self.__centered:
                offset -= round(self.dim[i] / 2)
            
            self.__pos[i] = half_surf_len + offset
                    


class Text(UIElement):
    
    def __init__(self, 
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
            self.DEFAULT_DIM,
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
        
    def createText(text: str, 
                   font: str, 
                   colour: tuple, 
                   size: int) -> pygame.Surface:
        
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
        
    def set_surf(self, surf_dim: tuple[int, int]):
            
        self._create_surf(
            surf_dim, 
            Text.createText(
                self.text,
                self.font, 
                globvar.get_colour(self.colour), 
                self.size))
        
        
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
        
        self.set_surf(surf_dim)
        


class Image(UIElement):
    
    def __init__(self, 
                 img_name: str,
                 scale: float = 1.0,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 **align_args: dict[str, bool]):
        
        super().__init__(
            self.DEFAULT_DIM,
            offset,
            alpha,
            centered,
            display,
            **align_args
        )
        
        self.img_name = img_name
        self.scale = scale
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        
        img_surf = globvar.get_img_surf(self.img_name)
        
        new_surf = pygame.transform.scale_by(img_surf, self.scale)
        
        self._create_surf(surf_dim, new_surf)
        
        
        
        
class Button:
    
    UNPRESS = "unpress"
    HOVER = "hover"
    PRESS = "press"
    __INVALID_STATE = f"State name doesn't match predefined states: '{UNPRESS}', '{HOVER}', '{PRESS}'."
    __INVALID_TYPE = "Invalid state added to button."
    
    
    def __init__(self, 
                 unpress_elem: UIElement,
                 hover_elem: UIElement = None,
                 press_elem: UIElement = None,
                 display: bool = True):
        
        self.__button_states = {
            self.UNPRESS: unpress_elem,
            self.HOVER: hover_elem,
            self.PRESS: press_elem
        }
        
        self.state = self.UNPRESS
        
        self.display = display
        
    
    def set_state(self, **ui_elements: dict[str, UIElement]):
        
        for state_name in ui_elements:
            
            if not Logger.raise_key_error(
                self.__button_states, state_name, self.__INVALID_STATE):
                
                if not Logger.raise_incorrect_type(
                    ui_elements[state_name], UIElement, self.__INVALID_TYPE):
                
                    self.__button_states[state_name] = ui_elements[state_name]
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        for state_name in self.__button_states:
            if self.__button_states[state_name] != None:
                self.__button_states[state_name].set_surf(surf_dim)
        
        
    def draw(self, surf: pygame.Surface):
        if self.__button_states[self.state] != None:
            self.__button_states[self.state].draw(surf)
        
    
    def set_pos(self, surf_dim: tuple[int, int]):
        for state_name in self.__button_states:
            if self.__button_states[state_name] != None:
                self.__button_states[state_name].set_pos(surf_dim)
                
        