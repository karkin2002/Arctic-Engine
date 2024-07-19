from typing import List, TypeVar

T = TypeVar('T')

def is_only_type(data: list[T] | tuple[T], data_type: T):
    """
    Check if all elements in the given data are of the specified data_type.
    
    Args:
        data (list or tuple): The data to be checked.
        data_type: The type to be checked against.
        
    Returns:
        bool: True if all elements in the data are of the specified data_type, 
        False otherwise.
    """
    return all(isinstance(item, data_type) for item in data)


def get_first_item_of_incorrect_type(data: list[T] | tuple[T], data_type: T):
    """
    Returns the first item in the given data that is not of the specified 
    data_type.
    
    Args:
        data (list[T] | tuple[T]): The data to search for the incorrect item.
        data_type (T): The expected data type of the items.
        
    Returns:
        T: The first item that is not of the specified data_type, or None if all 
        items are of the correct type.
    """
    return next((item for item in data if not isinstance(item, data_type)), None)


def is_point_in_rect(point_coords: tuple[int, int], 
                     rect_dims: tuple[int, int, int, int]) -> bool:
    """
    Check if a point is inside a rectangle.

    Args:
        point_coords (tuple[int, int]): Coordinates of the point (x, y).
        rect_dims (tuple[int, int, int, int]): Rectangle dimensions (x, y, 
        width, height).

    Returns:
        bool: True if the point is inside the rectangle, False otherwise.
    """
    x, y = point_coords
    rect_x, rect_y, rect_width, rect_height = rect_dims

    return rect_x <= x <= rect_x + rect_width and rect_y <= y <= rect_y + rect_height

def get_filename(file_path: str, include_extension: bool = True) -> str:
    """
    Extract the filename from a file path.

    Args:
        file_path (str): The file path.
        include_extension (bool, optional): Whether to include the file extension 
        in the filename. Defaults to True.

    Returns:
        str: The filename.
    """
    
    filename = file_path.split('/')[-1]

    if not include_extension:
        return filename.split('.')[0]

    return filename
    