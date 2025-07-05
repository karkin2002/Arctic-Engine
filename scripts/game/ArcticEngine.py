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
import pygame, scripts.utility.glob as glob
glob.init()


class ArcticEngine:

    __START_UP_INFO_TEXT = ("Initialising Arctic Engine. Draw time: {draw_time_ms}ms, Fixed update time:" +
                            "{fixed_update_time_ms}ms.")

    __events = 1 # Used for pygame timer event handling.

    def __init__(self,
                 win_dim: tuple[int, int] = (1280, 720),
                 draw_time_ms: int = 16,
                 fixed_update_time_ms: int = 100,
                 track_fps: bool = False):

        ## Window Essentials
        self.win_dim = win_dim
        self.win: pygame.Surface | None = None
        self.__set_win(win_dim)

        ## Components
        self.components: dict[str, Component] = {}

        ## Draw Time
        self.__draw_time_ms = draw_time_ms
        self.DRAW_EVENT = pygame.USEREVENT + self.__events
        self.__events += 1
        pygame.time.set_timer(self.DRAW_EVENT, self.__draw_time_ms)

        ## FPS counter
        self.track_fps = track_fps
        self.__fps_counter_start_time_ms: int = pygame.time.get_ticks()
        self.__fps_frame_counter: int = 0
        self.fps: int = 0

        ## Fixed Update Time
        self.__fixed_update_time_ms = fixed_update_time_ms
        self.FIXED_UPDATE_EVENT = pygame.USEREVENT + self.__events
        pygame.time.set_timer(self.FIXED_UPDATE_EVENT, self.__fixed_update_time_ms)

        ## Clock / Delta
        self.__clock = pygame.time.Clock()
        glob.update_delta_time()

        ## Logging
        Logger.log_info(self.__START_UP_INFO_TEXT.format(
            draw_time_ms=draw_time_ms,
            fixed_update_time_ms=fixed_update_time_ms))


    def handle_events(self):
        """
        This method handles the engines events, including update, fixed update, and drawing to the screen.

        TO-DO: Other events such as handling the quit button.
        """
        self.__update()

        for event in pygame.event.get():
            if event.type == self.FIXED_UPDATE_EVENT:
                self.__fixed_update()

            if event.type == self.DRAW_EVENT:
                self.__draw()


    def __draw(self):
        """
        Draws all components that have an implemented draw function.
        """
        for comp_ident, comp in self.components.items():
            comp.draw()

        pygame.display.flip()

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
        self.win_dim = win_dim
        self.win = pygame.display.set_mode(self.win_dim, pygame.RESIZABLE)


    def __set_fps(self):
        """
        Sets the fps counter. This method is called within the fixed update method, and therefore the speed at which the
        counter updates is tied to the frequency at which fixed update is called. Setting the fps can be disabled
        (with minor frame time boosts) using the track_fps parameter.
        """

        if self.track_fps:
            time_since_last_fixed_update_ms = pygame.time.get_ticks() - self.__fps_counter_start_time_ms

            self.fps = self.__fps_frame_counter // (time_since_last_fixed_update_ms / 1000)
            print(f"FPS: {self.fps}")

            self.__fps_counter_start_time_ms = pygame.time.get_ticks()
            self.__fps_frame_counter = 0

