from typing import TypeVar

T = TypeVar("T")

class ServiceLocator:

    __services: dict[any, any] = {}


    @classmethod
    def register(cls, key: type[T], instance: T):
        cls.__services[key] = instance


    @classmethod
    def get(cls, key: type[T]) -> T:
        try:
            return cls.__services[key]
        
        except KeyError:
            raise RuntimeError(f"Service not registered: {key.__name__}")


    @classmethod
    def clear(cls):
        cls.__services.clear()