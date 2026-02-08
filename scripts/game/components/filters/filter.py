from abc import abstractmethod, ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class Filter(Generic[T], ABC):

    @abstractmethod
    def apply(self, value: T) -> T:
        pass