import pygame

class UIElement:

    def __init__(self, dim):
        self.dim = dim


class UI:
    """Class for handeling the window and its UI
    """    
    
    def __init__(self, win_dim: tuple[int, int] = (700, 500)):
        """Constructor for UI class

        Args:
            win_dim (tuple[int, int], optional): Window h/w. Defaults to (700, 500).
        """        
        
        self.win_dim = None
        self.win = None

        self.__clock = pygame.time.Clock()
        
        self.__set_win(win_dim)


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

        self.win.fill((255, 255, 255))

        pygame.display.flip()

        self.__clock.tick(60)




window = UI()

pygame.init()

run = True

while run:

    if not window.events():
        run = False

    window.draw()


pygame.quit()
