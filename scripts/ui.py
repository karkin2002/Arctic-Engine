
import ctypes
from scripts.ui_element import UIElement, Button, Text
from scripts.logger import Logger
import pygame
import scripts.globvar as globvar
globvar.init()



## UI Class

class WindowUI:
    """Class for handeling the window and its UI
    """    
    
    __INVALID_TEXT_UPDATE = "Couldn't update text for '{elem_name}'."
    __OVERWRITTEN = "{data_type} '{name}' overwritten from '{pre_data}' to '{post_data}'."
    __ADDED_UI_ELEM = "UI Element '{name}' added as '{data_type}'."
    
    def __init__(self, win_dim: tuple[int, int] = (700, 500)):
        """Constructor for UI class

        Args:
            win_dim (tuple[int, int], optional): Window (<width>, <height>). Defaults to (700, 500).
        """        
        
        ctypes.windll.user32.SetProcessDPIAware() ## DON'T TURN THIS ON WITH FULLSCREEN
        
        self.win_dim: tuple[int, int] = None
        self.win: pygame.Surface = None

        self.__clock = pygame.time.Clock()
        
        self.__set_win(win_dim)
        self.resized: bool = False
        
        self.__ui_elems: dict[str, UIElement] = {}
        
        self.mouse_pos: tuple[int, int] = (0, 0)
        self.mouse_press: bool = False
        self.mouse_press_frames: int = 0


    def __set_win(self, win_dim: tuple[int, int]):
        """Creates a new window.

        Args:
            win_dim (tuple[int, int]): Window (<width>, <height>).
        """        

        self.win_dim = win_dim
        self.win = pygame.display.set_mode(self.win_dim, pygame.RESIZABLE)


    def events(self) -> bool:
        """Handles the window events, including resizing and quitting.

        Returns:
            bool: Whether the window is open.
        """
        
        self.resized = False

        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.mouse_press = True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_LEFT:
                self.mouse_press = False
                self.mouse_press_frames = 0
                
            
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.VIDEORESIZE:
                self.resized = True
                
        if self.mouse_press:
            self.mouse_press_frames += 1
        
        if self.resized:
            self.__resize()
                
        return True
    
    
    def draw(self):
        """Draws a new frame of the window; including all its elements.
        """
        
        self.win.fill((255, 255, 255))
        
        self.__draw_elems()

        pygame.display.flip()

        self.__clock.tick(60)
        
        
    def __resize(self):
        """Resizes the window, updating all its elements.
        """        
        
        self.win_dim = (self.win.get_width(), self.win.get_height())
        self.__resize_elems()
        

    
    def add_elem(self, 
                 elem_name: str, 
                 elem: UIElement | Button):
        """Adds a UI Element to be displayed on the window.

        Args:
            elem_name (str): Arbitrary name.
            elem (UIElement | Button): UI Element to be added.
        """     
        
        Logger.log_info(self.__ADDED_UI_ELEM.format(
            data_type = elem, name = elem_name))   
        
        if elem_name in self.__ui_elems:
            Logger.log_warning(self.__OVERWRITTEN.format(
                data_type = UIElement,
                name = elem_name,
                pre_data = self.__ui_elems[elem_name],
                post_data = elem
            ))
            
        self.__ui_elems[elem_name] = elem
        
        self.__ui_elems[elem_name].set_surf(self.win_dim)
        
        
    def get_elem(self, elem_name: str) -> UIElement | Button:
        """Returns an UI element from an element name

        Args:
            elem_name (str): element name.

        Returns:
            UIElement | Button: The UI element.
        """        
        
        return self.__ui_elems[elem_name]

        
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
            
    
    def is_pressed(self, elem_name: str, hold: bool = False) -> bool:
        """
        Checks if a UI element is pressed.

        Args:
            elem_name (str): The name of the UI element.
            hold (bool, optional): Whether to check for a single press or a 
            continuous hold. Defaults to False.

        Returns:
            bool: True if the UI element is pressed, False otherwise.
        """

        
        ui_elem = self.get_elem(elem_name)
        
        if type(ui_elem) == UIElement:
            intersects = ui_elem.intersects(self.mouse_pos)
            
        elif type(ui_elem) == Button:
            intersects = ui_elem.intersects(self.mouse_pos, self.mouse_press)
        
        else:
            intersects = False
            
            
        if hold:
            return intersects and self.mouse_press
        
        else:
            return intersects and self.mouse_press_frames == 1
    
    
    
    def update_text(self, 
                    elem_name: str,
                    text: str = None, 
                    font: str = None, 
                    colour: int = None):
        """
        Update the text of a UI element.

        Args:
            elem_name (str): The name of the UI element.
            text (str, optional): The new text to be set. Defaults to None.
            font (str, optional): The new font of the text. Defaults to None.
            colour (int, optional): The new colour of the text. Defaults to 
            None.
        """
        
        text_elem = self.get_elem(elem_name)
        
        if not Logger.raise_incorrect_type(
                text_elem, 
                Text, 
                self.__INVALID_TEXT_UPDATE.format(elem_name = elem_name)):
            
            text_elem.update_text(self.win_dim, 
                                  text, 
                                  font, 
                                  colour)