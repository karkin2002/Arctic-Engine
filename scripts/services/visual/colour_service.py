from scripts.utility.logger import Logger

class ColourService:

    __COLOUR_REPLACED = "Colour '{colour_name}' already exists. Value {pre_colour_value} replaced by {post_colour_value}."
    __COLOUR_ADDED = "Colour '{colour_name}' added as {colour_value}."
    __INVALID_COLOUR_VALUE = "Colour '{colour_name}' has an invalid colour value {colour_value}."
    __COLOUR_DOES_NOT_EXIST = "Colour '{colour_name}' does not exist."
    __COLOUR_REMOVED = "Colour '{colour_name}' has been removed."

    ERROR_COLOUR_VALUE = (255, 0, 220)
    OUTLINE_COLOUR_VALUE = (255, 0, 0)


    def __init__(self):
        self.__colour_dict = {}


    def __is_valid_colour(self, colour_name: str, colour: tuple) -> bool:
        if (
                not Logger.raise_incorrect_len(colour, 3, self.__INVALID_COLOUR_VALUE.format(
                    colour_name = colour_name, colour_value = colour)) and
                not Logger.raise_incorrect_type(colour, tuple, self.__INVALID_COLOUR_VALUE.format(
                    colour_name = colour_name, colour_value = colour))):

            if type(colour[0]) is int and type(colour[1]) is int and type(colour[2]) is int:
                return True

            else:
                Logger.raise_exception(self.__INVALID_COLOUR_VALUE.format(colour_name = colour_name, colour_value = colour))

        return False



    def add_colour(self, colour_name: str, colour: tuple[int, int, int]) -> bool:

        if self.__is_valid_colour(colour_name, colour):

            if colour_name in self.__colour_dict:
                Logger.log_warning(self.__COLOUR_REPLACED.format(colour_name=colour_name, pre_colour_value=self.__colour_dict[colour_name], post_colour_value=colour))

            else:
                Logger.log_info(self.__COLOUR_ADDED.format(colour_name=colour_name, colour_value=colour))

            self.__colour_dict[colour_name] = colour

            return True

        return False



    def get_colour(self, colour_name: str) -> tuple[int, int, int]:

        if not Logger.raise_key_error(self.__colour_dict,
                                      colour_name,
                                      self.__COLOUR_DOES_NOT_EXIST.format(colour_name = colour_name),
                                      False):

            return self.__colour_dict[colour_name]


        else:
            return self.ERROR_COLOUR_VALUE



    def remove_colour(self, colour_name: str) -> bool:

        if colour_name in self.__colour_dict:
            del self.__colour_dict[colour_name]
            Logger.log_info(self.__COLOUR_REMOVED.format(colour_name=colour_name))
            return True

        else:
            Logger.log_info(self.__COLOUR_DOES_NOT_EXIST.format(colour_name=colour_name))
            return False
