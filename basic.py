from typing import List, TypeVar

T = TypeVar('T')

def is_only_type(data: list[T] | tuple[T], data_type: T):
    return all(isinstance(item, data_type) for item in data)

def get_first_item_of_incorrect_type(data: list[T] | tuple[T], data_type: T):
    return next((item for item in data if not isinstance(item, data_type)), None)

