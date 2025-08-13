__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from scripts.utility.logger import Logger
from scripts.game.components.component import Component
from scripts.game.time import Time
from scripts.services.service_locator import ServiceLocator
from scripts.game.components.camera.camera import Camera
import pygame, scripts.utility.glob as glob
glob.init()


class ArcticEngine:

    __START_UP_INFO_TEXT = "Initialising Arctic Engine."

    __INVALID_CAMERA_TEXT = ("{camera_ident} is not a valid camera. Please ensure the component you are setting as the" +
                             "camera exists as a component and is of type Camera object.")
    __CAMERA_SET_NONE_TEXT = "Camera has been unset."
    __CAMERA_SET_TEXT = "Camera has been set to '{camera_ident}'."

    def __init__(self,
                 win_dim: tuple[int, int] = (1280, 720),
                 framerate: int = 60,
                 update_time_ms: int = 20,
                 background: str | None = None):

        ## Logging
        Logger.log_info(self.__START_UP_INFO_TEXT)

        ## Window Essentials
        self.win_dim = win_dim
        self.win_center = (0, 0)
        self.win: pygame.Surface | None = None
        self.__set_win(win_dim)
        self.background = background

        ## Components
        self.components: dict[str, Component] = {}

        ## Clock / Framerate
        self.time = Time(framerate, update_time_ms)
        ServiceLocator.register(Time, self.time)

        ## Camera
        # Setting camera to the identifier for a Camera object stored in the components dictionary, applies those
        # camera's modifiers to the screen / components (e.g. move everything to the left, the center is the center
        # of the window).
        self.__camera: str | None = None




    def handle_events(self) -> bool:
        """
        This method handles the engines events, including update, fixed update, and drawing to the screen.

        TO-DO: Other events such as handling the quit button.

        Returns:
            bool: True if the engine is still running, False otherwise.
        """

        glob.update_delta_time()

        for event in pygame.event.get():

            if event.type == pygame.VIDEORESIZE:
                self.__resize()

            if event.type == pygame.QUIT:
                return False

        return True


    def update(self):
        """
        Updates all components that have an implemented update function & updates the clock. This method runs every frame.
        """

        self.time.tick()

        while self.time.is_update():
            for comp_ident, comp in self.components.items():
                comp.update()


    def draw(self):
        """
        Draws all components that have an implemented draw function.
        """

        ## Drawing background
        if self.background is not None:
            self.win.fill(glob.get_colour(self.background))


        ## Drawing Components
        for comp_ident, comp in self.components.items():

            comp_surf = comp.draw()

            if comp_surf is not None:

                ## Centering xy 00 to center of screen
                comp_coord = (comp.pos[0] + self.win_center[0], comp.pos[1] + self.win_center[1])

                ## Adding camera position
                if self.__camera is not None:
                    camera = self.components[self.__camera]
                    comp_coord = (comp_coord[0] + camera.pos[0], comp_coord[1] + camera.pos[1])

                ## Drawing the surface to the screen
                self.win.blit(comp_surf, comp_coord)

        ## Updating Display
        pygame.display.flip()




    def __set_win(self, win_dim: tuple[int, int]):
        """Creates a new window.

        Args:
            win_dim (tuple[int, int]): Window (<width>, <height>).
        """
        self.win = pygame.display.set_mode(win_dim, pygame.RESIZABLE)
        self.__resize()


    def __resize(self):
        """
        Handles the event upon which the window is resized.
        """
        self.win_dim = self.win.get_size()
        self.win_center = (round(self.win_dim[0] / 2), round(self.win_dim[1] / 2))


    def set_camera(self, camera_ident: str | None):
        """
        Sets the camera to a specified camera component.
        """

        if camera_ident is None:
            self.__camera = camera_ident
            Logger.log_warning(self.__CAMERA_SET_NONE_TEXT)
            return

        elif camera_ident in self.components:
            if isinstance(self.components[camera_ident], Camera):
                self.__camera = camera_ident
                Logger.log_info(self.__CAMERA_SET_TEXT.format(camera_ident=camera_ident))
                return

        Logger.log_error(self.__INVALID_CAMERA_TEXT.format(camera_ident=camera_ident))


    def get_camera_ident(self) -> str | None:
        return self.__camera

