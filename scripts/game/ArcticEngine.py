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
from scripts.game.components.Component import Component
from scripts.game.components.camera.Camera import Camera
import pygame, scripts.utility.glob as glob
glob.init()


class ArcticEngine:

    __START_UP_INFO_TEXT = ("Initialising Arctic Engine. Draw time: {draw_time_ms}ms, Fixed update time:" +
                            "{fixed_update_time_ms}ms.")

    __INVALID_CAMERA_TEXT = ("{camera_ident} is not a valid camera. Please ensure the component you are setting as the" +
                             "camera exists as a component and is of type Camera object.")
    __CAMERA_SET_NONE_TEXT = "Camera has been unset."
    __CAMERA_SET_TEXT = "Camera has been set to '{camera_ident}'."

    __events = 1 # Used for pygame timer event handling.

    def __init__(self,
                 win_dim: tuple[int, int] = (1280, 720),
                 draw_time_ms: int = 16,
                 fixed_update_time_ms: int = 20,
                 track_fps: bool = False,
                 background: str | None = None):

        ## Window Essentials
        self.win_dim = win_dim
        self.win_center = (0, 0)
        self.win: pygame.Surface | None = None
        self.__set_win(win_dim)
        self.background = background

        ## Components
        self.components: dict[str, Component] = {}

        ## Draw Time
        self.__draw_time_ms = draw_time_ms
        self.DRAW_EVENT = pygame.USEREVENT + self.__events
        self.__events += 1
        pygame.time.set_timer(self.DRAW_EVENT, self.__draw_time_ms)

        ## Fixed Update Time
        self.__fixed_update_time_ms = fixed_update_time_ms
        self.FIXED_UPDATE_EVENT = pygame.USEREVENT + self.__events
        pygame.time.set_timer(self.FIXED_UPDATE_EVENT, self.__fixed_update_time_ms)

        ## Clock / Delta
        self.__clock = pygame.time.Clock()
        glob.update_delta_time()

        ## FPS counter
        self.track_fps = track_fps
        self.__fps_counter_start_time_ms: int = pygame.time.get_ticks()
        self.__fps_frame_counter: int = 0
        self.fps: int = 0

        ## Camera
        # Setting camera to the identifier for a Camera object stored in the components dictionary, applies those
        # camera's modifiers to the screen / components (e.g. move everything to the left, the center is the center
        # of the window).
        self.__camera: str | None = None

        ## Logging
        Logger.log_info(self.__START_UP_INFO_TEXT.format(
            draw_time_ms=draw_time_ms,
            fixed_update_time_ms=fixed_update_time_ms))


    def handle_events(self) -> bool:
        """
        This method handles the engines events, including update, fixed update, and drawing to the screen.

        TO-DO: Other events such as handling the quit button.

        Returns:
            bool: True if the engine is still running, False otherwise.
        """
        self.__update()

        for event in pygame.event.get():
            if event.type == self.FIXED_UPDATE_EVENT:
                self.__fixed_update()

            if event.type == self.DRAW_EVENT:
                self.__draw()

            if event.type == pygame.VIDEORESIZE:
                self.__resize()

            if event.type == pygame.QUIT:
                return False

        return True


    def __draw(self):
        """
        Draws all components that have an implemented draw function.
        """
        glob.update_delta_time()

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

        ## Tracking number of frames drawn
        if self.track_fps:
            self.__fps_frame_counter += 1



    def __update(self):
        """
        Updates all components that have an implemented update function. This method runs every frame.
        """
        for comp_ident, comp in self.components.items():
            comp.update()


    def __fixed_update(self):
        """
        Updates all components that have an implemented fixed update function. This method runs every fixed number of
        ms.
        """
        for comp_ident, comp in self.components.items():
            comp.fixed_update()

        self.__set_fps()


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


    def __set_fps(self):
        """
        Sets the fps counter. This method is called within the fixed update method, and therefore the speed at which the
        counter updates is tied to the frequency at which fixed update is called. Setting the fps can be disabled
        (with minor frame time boosts) using the track_fps parameter.
        """

        if self.track_fps:
            time_since_last_fixed_update_ms = pygame.time.get_ticks() - self.__fps_counter_start_time_ms
            self.__fps_counter_start_time_ms = pygame.time.get_ticks()
            self.fps = self.__fps_frame_counter // (time_since_last_fixed_update_ms / 1000)
            self.__fps_frame_counter = 0

            print(f"FPS: {self.fps} time_since_last_fixed_update_ms: {time_since_last_fixed_update_ms}")


    def set_camera(self, camera_ident: str | None):
        if camera_ident is None:
            self.__camera = camera_ident
            Logger.log_warning(self.__CAMERA_SET_NONE_TEXT)
            return

        if camera_ident in self.components:
            if isinstance(self.components[camera_ident], Camera):
                self.__camera = camera_ident
                Logger.log_info(self.__CAMERA_SET_TEXT.format(camera_ident=camera_ident))
                return

        Logger.log_error(self.__INVALID_CAMERA_TEXT.format(camera_ident=camera_ident))

    def get_camera_ident(self) -> str | None:
        return self.__camera

