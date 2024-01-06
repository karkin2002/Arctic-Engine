
import ctypes
from ui_element import UIElement, Text
from logger import Logger
import pygame
import globvar
globvar.init()



## UI Class

class WindowUI:
    """Class for handeling the window and its UI
    """    
    
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
        
        self.__ui_elems[elem_name] = UIElement(self.win_dim, 
                                               dim, 
                                               offset, 
                                               alpha,
                                               centered, 
                                               display,
                                               **align_args)
        
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

        self.__ui_elems[elem_name] = Text(
            self.win_dim, 
            text,
            size,
            font,
            colour,
            offset,
            alpha,
            centered,
            display,
            **align_args)

        
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

globvar.add_colour("RED", (255, 0, 0))
window = WindowUI((1920, 1080))

window.add_text(
    "text_test", 
    "GUI Organisation Test", 
    100, 
    "verdana", 
    "RED", 
    offset = (0, 80),
    align_up = True)

window.add_text(
    "player_name", 
    "Arctic Survival Build 1.0", 
    15, 
    "verdana", 
    "RED", 
    centered=False,
    align_up = True,
    align_left = True)


run = True
while run:

    if not window.events():
        run = False

    window.draw()

pygame.quit()