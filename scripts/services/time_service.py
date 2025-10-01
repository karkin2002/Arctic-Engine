from scripts.utility.logger import Logger
from pygame import time as pygame_time

class Time:

    INIT_MESSAGE = "Initialising Time. Framerate: {framerate}FPS, Update Time: {update_time_ms}ms."
    __STABLE_FRAMERATE_SET_TEXT = "Stable framerate set to '{stable_framerate}'."

    def __init__(self,
                 framerate: int = 60,
                 update_time_ms: float = 20.0,
                 stable_framerate = False):
        """
        Initializes the class with provided framerate, update time, and stable framerate
        settings.

        Parameters:
            framerate: The targeted frame rate for the application in frames per second.
            update_time_ms: The amount of time allocated for each update cycle, in milliseconds.
            stable_framerate: Determines whether framerate stability will be enforced
                              (default is False).
        """

        Logger.log_info(self.INIT_MESSAGE.format(
            framerate=framerate,
            update_time_ms=update_time_ms))

        self.__clock = pygame_time.Clock()
        self.framerate = framerate
        self.update_time_ms = update_time_ms
        self.fixed_delta_time = update_time_ms / 1000.0

        self.__tick_method = None
        self.set_stable_framerate(stable_framerate)

        self.elapsed_time = 0.0
        self.lag = 0.0
        self.interpolated_time = 0.0


    def set_stable_framerate(self, stable_framerate: bool):
        """
        Sets whether the frame rate should be kept stable during the game's execution.
        Switches between employing a more CPU-intensive but stable tick method or a less
        demanding standard tick.

        Args:
            stable_framerate: A boolean that, if True, selects a stable frame rate
            using a busy loop method; otherwise, a standard tick method is used.
        """

        if stable_framerate:
            self.__tick_method = self.__clock.tick_busy_loop
        else:
            self.__tick_method = self.__clock.tick

        Logger.log_info(self.__STABLE_FRAMERATE_SET_TEXT.format(stable_framerate=stable_framerate))


    def tick(self):
        """
        Updates the time values. Should be run every frame.
        """
        self.elapsed_time = self.__tick_method(self.framerate)
        self.lag += self.elapsed_time
        self.interpolated_time = self.lag / self.update_time_ms


    def is_update(self) -> bool:
        """
        Determines if the system requires an update based on time lag.

        This method checks if the accumulated lag has reached or exceeded
        the update threshold (`update_time_ms`). If so, it decreases the lag
        by the update interval and returns True. Otherwise, it returns False.

        Returns:
            bool: True if the system requires an update, False otherwise.
        """
        if self.lag >= self.update_time_ms:
            self.lag -= self.update_time_ms
            self.interpolated_time = self.lag / self.update_time_ms
            return True
        return False


    def get_fps(self) -> float:
        """
        Gets the current frame-per-second (FPS).

        Returns:
            float: The current frames per second as calculated by the clock.
        """

        return self.__clock.get_fps()
