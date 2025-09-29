from scripts.utility.logger import Logger
from pygame import surface as surface, time as py_time


class Image:

    __IMAGE_INIT_TEXT = "New image '{image_name}' created at timestamp: {timestamp}."

    def __init__(self,
                 image_name: str,
                 image_surface: surface):

        self.image_name = image_name
        self.surface = image_surface
        self.timestamp = py_time.get_ticks()

        Logger.log_info(self.__IMAGE_INIT_TEXT.format(image_name=image_name, timestamp=self.timestamp))




class ImageService:

    __IMAGE_ALREADY_EXISTS = "Image '{image_name}' already exists. Image not created."
    __INVALID_IMAGE_NAME = "Image '{image_name}' doesn't exist."
    __IMAGE_DELETED = "Image '{image_name}' deleted."
    __TEMP_IMAGE_DELETED = "Image '{image_name}' deleted due to expired lifespan."

    def __init__(self,
                 temp_image_lifespan_ms: float = 600000):

        self.__image_dict: dict[str, Image] = {}

        self.__temp_image_dict: dict[str, Image] = {}
        self.temp_image_lifespan_ms = temp_image_lifespan_ms


    def add_image(self,
                  image_name: str,
                  image_surface: surface,
                  temp_image: bool = False):

        if image_name not in self.__image_dict and image_name not in temp_image:
            if temp_image:
                self.__temp_image_dict[image_name] = Image(image_name, image_surface)

            else:
                self.__image_dict[image_name] = Image(image_name, image_surface)

        else:
            Logger.log_warning(self.__IMAGE_ALREADY_EXISTS.format(image_name=image_name))


    def delete_image(self, image_name: str):

        if image_name in self.__image_dict:
            del self.__image_dict[image_name]
            Logger.log_info(self.__IMAGE_DELETED.format(image_name=image_name))

        elif image_name in self.__temp_image_dict:
            del self.__temp_image_dict[image_name]
            Logger.log_info(self.__IMAGE_DELETED.format(image_name=image_name))

        else:
            Logger.log_warning(self.__INVALID_IMAGE_NAME.format(image_name=image_name))


    def delete_first_temp_image_by_lifespan(self):

        if len(self.__temp_image_dict) > 0:
            first_image_name = next(iter(self.__temp_image_dict))

            if self.__temp_image_dict[first_image_name].timestamp >= self.temp_image_lifespan_ms:
                self.delete_image(first_image_name)
                Logger.log_info(self.__TEMP_IMAGE_DELETED.format(image_name=first_image_name))