from pygame import time as py_time
from scripts.utility.logger import Logger
from scripts.services.service_locator import ServiceLocator
from scripts.services.visual.image_service import ImageService


class Animation:

    __IMAGE_DOES_NOT_EXIST = "Image '{image_name}' does not exist. Animation frames could not be set."
    __NEW_FRAMES_SET = "Animation frames set to {frames}."

    def __init__(self, frames: list[str], animation_length_ms: int = 1000, repeat = True):

        self.__frames: list[str] = []
        self.__image_service = ServiceLocator.get(ImageService)

        self.animation_length_ms: int = animation_length_ms
        self.repeat: bool = repeat

        self.__start_time: int = py_time.get_ticks()
        self.finished = False

        self.set_frames(frames)



    def set_frames(self, frames: list[str]) -> bool:

        for image_name in frames:

            if not self.__image_service.is_image(image_name):

                Logger.log_error(self.__IMAGE_DOES_NOT_EXIST.format(image_name=image_name))

                return False

        self.__frames = frames
        Logger.log_info(self.__NEW_FRAMES_SET.format(frames=self.__frames))

        return True



    def get_current_frame(self) -> str | None:

        if not self.__frames:
            return None

        if not self.repeat and (py_time.get_ticks() - self.__start_time) >= self.animation_length_ms:
            self.finished = True
            return self.__frames[len(self.__frames) - 1]

        elapsed_time = (py_time.get_ticks() - self.__start_time) % self.animation_length_ms

        frame_duration = self.animation_length_ms / len(self.__frames)

        frame_index = int(elapsed_time // frame_duration)

        return self.__frames[frame_index]



    def reset(self):
        self.__start_time = py_time.get_ticks()
        self.finished = False











