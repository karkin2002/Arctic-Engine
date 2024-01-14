
import ctypes
from ui_element import UIElement, Text, Image, Button
from logger import Logger
import pygame
import globvar
globvar.init()



## UI Class

class WindowUI:
    """Class for handeling the window and its UI
    """    
    
    __INVALID_TYPE_UI_ELEM = "Invalid type when adding UI Element."
    __OVERWRITTEN = "{data_type} '{name}' overwritten from '{pre_data}' to '{post_data}'."
    
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
        
    def __add_to_elem_dict(self, elem_name:str, elem: UIElement):
        """Adds a UI Element to the UI Element dict.

        Args:
            elem_name (str): Arbitary name of UI Element.
            elem (UIElement): The UI Element.
        """        
        
        if not Logger.raise_incorrect_type(
            elem, UIElement, self.__INVALID_TYPE_UI_ELEM):
            
            if elem_name in self.__ui_elems:
                Logger.log_warning(self.__OVERWRITTEN.format(
                    data_type = UIElement,
                    name = elem_name,
                    pre_data = self.__ui_elems[elem_name],
                    post_data = elem
                ))
            
            self.__ui_elems[elem_name] = elem
        
        
    
    def add_elem(self, 
                 elem_name: str, 
                 dim: tuple[int, int], 
                 offset: tuple[int, int] = (0, 0), 
                 alpha: int = 255,
                 centered: bool = True, 
                 display: bool = True,
                 **align_args: dict[str, bool]):
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
        
        self.__add_to_elem_dict(elem_name, UIElement(self.win_dim, 
                                          dim, 
                                          offset, 
                                          alpha,
                                          centered, 
                                          display,
                                          **align_args))
        
    def add_text(self, 
                 elem_name: str, 
                 text: str,
                 size: str,
                 font: str,
                 colour: str,
                 offset: tuple[int, int] = (0, 0),
                 alpha: int = 255,
                 centered: bool = True,
                 display: bool = True,
                 **align_args: dict[str, bool]):

        self.__add_to_elem_dict(elem_name, Text(
            self.win_dim, 
            text,
            size,
            font,
            colour,
            offset,
            alpha,
            centered,
            display,
            **align_args))
        
    def add_img_surf(self,
                     elem_name: str,
                     img_name: str,
                     scale: float = 1.0,
                     offset: tuple[int, int] = (0, 0),
                     alpha: int = 255,
                     centered: bool = True,
                     display: bool = True,
                     **align_args: dict[str, bool]):
    
        self.__add_to_elem_dict(elem_name, Image(
            self.win_dim, 
            img_name,
            scale,
            offset,
            alpha,
            centered,
            display,
            **align_args))
        
        
    def add_button(self, 
                   elem_name: str, 
                   display: bool = True):
        
        self.__add_to_elem_dict(elem_name, Button(display=display))

        
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
            


































## Main Loop        
Logger("logs/UI_Organisation")  

pygame.init()


globvar.add_colour("BLACK", (0, 0, 0))

test_surf = pygame.Surface((200, 200))
test_surf.fill((100, 100, 200))
pygame.draw.rect(test_surf, (255, 0, 0), (0, 0, 100, 100))

globvar.add_img_surf("test_surf", test_surf)


window = WindowUI((1920, 1080))

window.add_img_surf("hello", "test_surf")

window.add_text(
    "text_test", 
    "GUI Organisation Test", 
    100, 
    "verdana", 
    "BLACK", 
    offset = (0, 80),
    align_top = True)

window.add_text(
    "player_name", 
    "Arctic Survival Build 1.0", 
    15, 
    "verdana", 
    "BLACK", 
    centered=False,
    align_top = True,
    align_left = True)

# window.add_button("button_test")


run = True
while run:

    if not window.events():
        run = False

    window.draw()

pygame.quit()