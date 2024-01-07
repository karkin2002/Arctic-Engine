from pygame import Surface
from basic import is_only_type, get_first_item_of_incorrect_type
from logger import Logger



def init():
    
    ## Global Colour Dictonary Variables
    global glob_colour_dict
    glob_colour_dict = {}
    
    ## Global Image Dictonary Variables
    global glob_img_dict
    glob_img_dict = {}
    

OVERWRITTEN = "{data_type} '{name}' overwritten from '{pre_data}' to '{post_data}'."
ADDED_TO_DICT = "{data_type} '{name}' added as '{data}'."

COLOUR = "Colour"
INVALID_COLOUR_VALUE = "Invalid colour value."
INVALID_COLOUR_NAME = "Invalid colour name."

IMG = "Image"
INVALID_IMG_SURF = "Invalid image surface."
INVALID_IMG_NAME = "Invalid imgage name."


def add_colour(colour_name: str, colour: tuple[int, int, int]):
    """Adds a new colour to the global colour dictonary.

    Args:
        colour_name (str): Arbitrary name of the colour.
        colour (tuple[int, int, int]): Colour as (<red_value>, <green_value>,
        <blue_value>)
    """        
    
    if ((not Logger.raise_incorrect_type(colour, tuple, INVALID_COLOUR_VALUE)) and 
        (not Logger.raise_incorrect_len(colour, 3, INVALID_COLOUR_VALUE)) and 
        is_only_type(colour, int)):
        
        if colour_name in glob_colour_dict:
            Logger.log_warning(
                OVERWRITTEN.format(
                    data_type = COLOUR,
                    name = colour_name,
                    pre_data = glob_colour_dict[colour_name],
                    post_data = colour))
        
        glob_colour_dict[colour_name] = colour
        
        Logger.log_info(ADDED_TO_DICT.format(
            data_type = COLOUR,
            name = colour_name,
            data = colour))
    
    else:        
        Logger.raise_incorrect_type(
            get_first_item_of_incorrect_type(colour, int), 
            int,
            INVALID_COLOUR_VALUE)
            

def get_colour(colour_name: str) -> tuple[int, int, int]:
    """Returns a colour from a name

    Args:
        colour_name (str): Name of the colour.

    Returns:
        tuple[int, int, int]: Colour.
    """    
    
    if not Logger.raise_key_error(glob_colour_dict, 
                                  colour_name,
                                  INVALID_COLOUR_NAME):
        
        return glob_colour_dict[colour_name]
    

def add_img_surf(img_name: str, img_surf: Surface):
    """Adds a new surface to the global image dictonary.

    Args:
        img_name (str): Arbitrary name of the surface.
        img_surf (Surface): Surface to be added.
    """    
    
    if not Logger.raise_incorrect_type(img_surf, Surface, INVALID_IMG_SURF):
        
        if img_name in glob_img_dict:
            Logger.log_warning(
                OVERWRITTEN.format(
                    data_type = "Image",
                    name = img_name,
                    pre_data = glob_img_dict[img_name],
                    post_data = img_surf))
        
        glob_img_dict[img_name] = img_surf
        
        Logger.log_info(ADDED_TO_DICT.format(
            data_type = IMG,
            name = img_name,
            data = img_surf))
        
        
def get_img_surf(img_name: str) -> Surface:
    """Reutnrs a surface from a name

    Args:
        img_name (str): Name of the surface.

    Returns:
        Surface: Surface.
    """    
    
    if not Logger.raise_key_error(glob_img_dict, 
                                  img_name,
                                  INVALID_IMG_NAME):
    
        return glob_img_dict[img_name]