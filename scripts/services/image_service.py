from scripts.utility.logger import Logger
from pygame import surface as surface, time as py_time, Surface


class Image:

    __IMAGE_INIT_TEXT = "New image '{image_name}' created at timestamp: {timestamp} ms."

    def __init__(self,
                 image_name: str,
                 image_surface: surface):

        self.image_name = image_name
        self.surface = image_surface
        self.dim = image_surface.get_size()
        self.timestamp = py_time.get_ticks()

        Logger.log_info(self.__IMAGE_INIT_TEXT.format(image_name=image_name, timestamp=self.timestamp))




class ImageService:

    __IMAGE_SERVICE_START = "Image Service Started. Temp Image Lifespan: {temp_image_lifespan} ms."
    __IMAGE_ALREADY_EXISTS = "Image '{image_name}' already exists. Image not created."
    __INVALID_IMAGE_NAME = "Image '{image_name}' doesn't exist."
    __IMAGE_DELETED = "Image '{image_name}' deleted at timestamp: {timestamp} ms."
    __TEMP_IMAGE_DELETED = "Image '{image_name}' lifespan expired."

    def __init__(self,
                 temp_image_lifespan_ms: float = 600000):

        self.__image_dict: dict[str, Image] = {}

        self.__temp_image_dict: dict[str, Image] = {}
        self.temp_image_lifespan_ms = temp_image_lifespan_ms

        Logger.log_info(self.__IMAGE_SERVICE_START.format(temp_image_lifespan=temp_image_lifespan_ms))



    def add_image(self,
                  image_name: str,
                  image_surface: surface,
                  temp_image: bool = False):
        """
        Adds a new image to the image dict.

        Parameters:
            image_name (str): The name of the image.
            image_surface (Surface): The surface of the image.
            temp_image (bool): If True the image will be temporary dependent on lifespan. Otherwise, the image will be
            permanent until deleted. Defaults to False.
        """

        if image_name not in self.__image_dict and image_name not in self.__temp_image_dict:
            if temp_image:
                self.__temp_image_dict[image_name] = Image(image_name, image_surface)

            else:
                self.__image_dict[image_name] = Image(image_name, image_surface)

        else:
            Logger.log_warning(self.__IMAGE_ALREADY_EXISTS.format(image_name=image_name))



    def delete_image(self, image_name: str):
        """
        Deletes an image from the image dict.

        Parameters:
            image_name (str): The name of the image.
        """

        if image_name in self.__image_dict:
            del self.__image_dict[image_name]
            Logger.log_info(self.__IMAGE_DELETED.format(image_name=image_name, timestamp=py_time.get_ticks()))

        elif image_name in self.__temp_image_dict:
            del self.__temp_image_dict[image_name]
            Logger.log_info(self.__IMAGE_DELETED.format(image_name=image_name, timestamp=py_time.get_ticks()))

        else:
            Logger.log_warning(self.__INVALID_IMAGE_NAME.format(image_name=image_name))



    def get_image(self, image_name: str) -> Image | None:
        """
        Gets an image from the image dict.

        Parameters:
            image_name (str): The name of the image.

        Returns:
            Image | None if the image does not exist.
        """

        if image_name in self.__image_dict:
            return self.__image_dict[image_name]

        elif image_name in self.__temp_image_dict:
            return self.__temp_image_dict[image_name]

        else:
            Logger.log_critical(self.__INVALID_IMAGE_NAME.format(image_name=image_name))




    def delete_first_temp_image_by_lifespan(self):
        """
        PROOF OF CONCEPT - DON'T USE THIS METHOD YET. It doesn't preform as planned. The idea is that when an image
        hasn't been used for a period of time, the image is deleted from memory, but it's file location is stored ready
        to be read whenever necessary.

        This method checks the first image in the image dict and deletes it.
        """

        if len(self.__temp_image_dict) > 0:
            first_image_name = next(iter(self.__temp_image_dict))

            if py_time.get_ticks() - self.__temp_image_dict[first_image_name].timestamp >= self.temp_image_lifespan_ms:

                Logger.log_info(self.__TEMP_IMAGE_DELETED.format(image_name=first_image_name))

                self.delete_image(first_image_name)