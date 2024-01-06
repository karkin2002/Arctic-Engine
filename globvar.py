from basic import is_only_type, get_first_item_of_incorrect_type
from logger import Logger



def init():
    global INCORRECT_COLOUR_VALUE_TEXT, INCORRECT_COLOUR_NAME_TEXT
    global glob_colour_dict
    
    glob_colour_dict = {}
    
    INCORRECT_COLOUR_VALUE_TEXT = "Invalid colour value."
    INCORRECT_COLOUR_NAME_TEXT = "Invalid colour name."
    
    
    
def add_colour(colour_name: str, colour: tuple[int, int, int]):
    """Adds a new colour to glob_colour_dict.

    Args:
        colour_name (str): Arbitrary name of the colour.
        colour (tuple[int, int, int]): Colour as (<red_value>, <green_value>,
        <blue_value>)
    """        
    
    if ((not Logger.raise_incorrect_type(colour, tuple, INCORRECT_COLOUR_VALUE_TEXT)) and 
        (not Logger.raise_incorrect_len(colour, 3, INCORRECT_COLOUR_VALUE_TEXT)) and 
        is_only_type(colour, int)):
        
        glob_colour_dict[colour_name] = colour
    
    else:        
        Logger.raise_incorrect_type(
            get_first_item_of_incorrect_type(colour, int), 
            int,
            INCORRECT_COLOUR_VALUE_TEXT)
            

def get_colour(colour_name: str) -> tuple[int, int, int]:
    """Returns a colour from a name

    Args:
        colour_name (str): Name of the colour.

    Returns:
        tuple[int, int, int]: Colour.
    """    
    
    if not Logger.raise_key_error(glob_colour_dict, 
                                  colour_name,
                                  INCORRECT_COLOUR_NAME_TEXT):
        
        return glob_colour_dict[colour_name]
    

        