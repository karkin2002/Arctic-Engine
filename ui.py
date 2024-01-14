
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
                 elem: UIElement):
        """Adds a UI Element to be displayed on the window.

        Args:
            elem_name (str): Arbitrary name.
            elem (UIElement): The UI Element.
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

window.add_elem("hello", 
                Image("test_surf", align_right = True))

window.add_elem("text_test",
                Text("GUI Organisation Test",
                     100, 
                     "verdana", 
                     "BLACK", 
                     offset = (0, 80),
                     align_top = True))

window.add_elem("player_name",
                Text("Arctic Survival Build 1.0", 
                     15, 
                     "verdana", 
                     "BLACK", 
                     centered=False,
                     align_top = True,
                     align_left = True))



p_text = Text("test",100,"verdana", "BLACK") 
h_text = Text("test",100,"verdana", "BLACK")
u_text = Text("test",100,"verdana", "BLACK")  
window.add_elem("test_button", Button(p_text, h_text, u_text))


run = True
while run:

    if not window.events():
        run = False

    window.draw()

pygame.quit()