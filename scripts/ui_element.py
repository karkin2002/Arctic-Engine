import pygame
from pygame import font as pyfont
from scripts.logger import Logger
import scripts.globvar as globvar
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
        self.__in_surf_bounds = True
        
        
    def set_display(self, display: bool):
        """Sets whether the UIElement should be displayed.

        Args:
            display (bool): True to display the UIElement, False to hide it.
        """
        self.__display = display
        
        
    def get_display(self) -> bool:
        """Returns whether the UIElement is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """
        return self.__display
        
        
        
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
        return (self.__display and 
                self.__alpha > 0 and 
                self.__surf != None and 
                self.__in_surf_bounds)
    
    
    def __set_in_surf_bounds(self, surf_dim: tuple[int, int]):
        """Sets whether the UIElement is visible on the surface.

        Args:
            surf_dim (tuple[int, int]): (<width>, <height>) of the surface to be 
            drawn on.
        """        
        
        self.__in_surf_bounds = (self.__pos[0] + self.dim[0] >= 0 and
                                 self.__pos[0] <= surf_dim[0] and
                                 self.__pos[1] + self.dim[1] >= 0 and
                                 self.__pos[1] <= surf_dim[1])
            
        
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
            
        self.__set_in_surf_bounds(surf_dim)
        
        
    def intersects(self, pos: tuple[int, int]) -> bool:
        """Returns whether pos is within the ui element.

        Args:
            pos (tuple[int, int]): The position to check.

        Returns:
            bool: True if pos is within the object's dimensions, False 
            otherwise.
        """
        
        if self.__is_displayed:
            return (self.__pos[0] <= pos[0] <= self.__pos[0] + self.dim[0] and 
                    self.__pos[1] <= pos[1] <= self.__pos[1] + self.dim[1])
        
        else:
            return False
                    




class Text(UIElement):
    
    def __init__(self, 
                 text: str,
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
        self.font = font
        self.colour = colour
        
    def createText(text: str, 
                   font: str, 
                   colour: tuple) -> pygame.Surface:
        """Creates a surface with text on it.

        Args:
            text (str): Text to be drawn on the surface.
            font (str): Font of the text.
            colour (tuple): Colour of the text.

        Returns:
            pygame.Surface: Surface with text.
        """

        message = globvar.get_font(font).render(text, True, colour)

        return message
        
    def set_surf(self, surf_dim: tuple[int, int]):

        self._create_surf(
            surf_dim, 
            Text.createText(
                self.text,
                self.font, 
                globvar.get_colour(self.colour)
            )
        )
        
        
    def update_text(self, 
                        surf_dim: tuple[int, int],
                        text: str = None, 
                        font: str = None, 
                        colour: int = None):

            
            update = False
            
            if text != None and text != self.text: 
                self.text = text
                update = True
            
            if font != None and font != self.font: 
                self.font = font
                update = True
            
            if colour != None and colour != self.colour: 
                self.colour = colour
                update = True
            
            if update:
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
        
        if self.scale != 1:
            img_surf = pygame.transform.scale_by(img_surf, self.scale)
        
        self._create_surf(surf_dim, img_surf)
        
        
        
        
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
        
        self.__states = {
            self.UNPRESS: unpress_elem,
            self.HOVER: hover_elem,
            self.PRESS: press_elem
        }

        for state in self.__states.values():
            if state != None:
                state.set_display(False)
        
        self.current_state = self.UNPRESS
        
        self.set_display(display)
        


    def set_display(self, display: bool):
        """Sets whether the button should be displayed.

        Args:
            display (bool): The display value to set.
        """
        
        self.__display = display
        self.__states[self.current_state].set_display(display)
                    

    def get_display(self) -> bool:
        """Returns whether the Button is being displayed.

        Returns:
            bool: Whether it's being displayed.
        """
        return self.__display
        
    
    def set_state_ui_elem(self, **ui_elements: dict[str, UIElement]):
        
        for state_name in ui_elements:
            
            if not Logger.raise_key_error(
                self.__states, state_name, self.__INVALID_STATE):
                
                if not Logger.raise_incorrect_type(
                    ui_elements[state_name], UIElement, self.__INVALID_TYPE):
                
                    self.__states[state_name] = ui_elements[state_name]
                    
    
    def __set_curent_state(self, state_name: str):
        """Sets the current state of the button.

        Args:
            state_name (str): State name, predefined within Button class.
        """        
        
        if self.current_state != state_name:
            if not Logger.raise_key_error(
                self.__states, state_name, self.__INVALID_STATE):
                
                if self.__states[state_name] != None:
                    
                    self.__states[self.current_state].set_display(False)
                    self.current_state = state_name
                    if self.__display:
                        self.__states[self.current_state].set_display(True)
            
        
        
    def set_surf(self, surf_dim: tuple[int, int]):
        for state_name in self.__states:
            if self.__states[state_name] != None:
                self.__states[state_name].set_surf(surf_dim)
        
        
    def draw(self, surf: pygame.Surface):
        if self.__states[self.current_state] != None:
            self.__states[self.current_state].draw(surf)
        
    
    def set_pos(self, surf_dim: tuple[int, int]):
        for state_name in self.__states:
            if self.__states[state_name] != None:
                self.__states[state_name].set_pos(surf_dim)
                

    def intersects(self, pos: tuple[int, int], press: bool = False) -> bool:
        """
        Checks if the UI element intersects a given position.

        Args:
            pos (tuple[int, int]): The position of the click.
            press (bool, optional): The press state of the click. Defaults to 
            False.

        Returns:
            bool: True if the UI element is pressed, False otherwise.
        """
        
        if self.__states[self.UNPRESS].intersects(pos) and self.__display:
            
            if press:
                self.__set_curent_state(self.PRESS)
            
            elif self.__states[self.HOVER] != None:
                    self.__set_curent_state(self.HOVER)
            
            else:
                self.__set_curent_state(self.UNPRESS)
            
            return True
        
        self.__set_curent_state(self.UNPRESS)
        
        return False
    
    
    

class Group:
    
    __OVERWRITTEN = "{data_type} '{name}' in '{group_name}' overwritten from '{pre_data}' to '{post_data}'."
    __ADDED_UI_ELEM = "UI Element '{elem_name}' added to '{group_name}' as '{data}'."

    def __init__(self, name: str, display: bool = True):
        """
        Initializes a new instance of the UIElement class.
        """
        
        self.__NAME: str = name
        self.ui_elems: dict[str, UIElement] = {}
        
        self.display: bool = display
            
    def get_elem(self, elem_name: str) -> UIElement | Button:
        """
        Retrieves the UI element with the given name.

        Args:
            elem_name (str): The name of the UI element to retrieve.

        Returns:
            UIElement | Button: The UI element with the given name.

        """
        
        return self.ui_elems[elem_name]


    def add_elem(self, elem_name: str, elem: UIElement | Button):
        """
        Adds an element to the ui_elems dictionary.

        Args:
            elem_name (str): The name of the element.
            elem (UIElement | Button): The element to be added.
        """
        
        if elem_name in self.ui_elems:
            Logger.log_warning(self.__OVERWRITTEN.format(
                data_type = UIElement,
                name = elem_name,
                group_name = self.__NAME,
                pre_data = self.ui_elems[elem_name],
                post_data = elem
            ))
        
        self.ui_elems[elem_name] = elem
        
        Logger.log_info(self.__ADDED_UI_ELEM.format(
                elem_name = elem_name,
                group_name = self.__NAME,
                data = elem))


    def draw(self, surf: pygame.Surface):
        """
        Draws all UI elements on the given surface.

        Args:
            surf (Surface): The surface on which the UI elements will be drawn.
        """
        
        for elem_name in self.ui_elems:
            self.ui_elems[elem_name].draw(surf)