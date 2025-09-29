from typing import TypeVar
from scripts.utility.logger import Logger

T = TypeVar("T")

class ServiceLocator:

    __NEW_SERVICE_LOCATOR_REGISTERED = "New Service Locator Registered. Class name: '{service_name}'."
    __SERVICE_LOCATOR_ALREADY_EXISTS = "Service Locator '{service_name}' already registered."

    __services: dict[any, any] = {}


    @classmethod
    def register(cls, key: type[T], instance: T):

        if key in cls.__services:
            Logger.log_warning(ServiceLocator.__SERVICE_LOCATOR_ALREADY_EXISTS.format(service_name=key.__name__))

        else:
            cls.__services[key] = instance
            Logger.log_info(ServiceLocator.__NEW_SERVICE_LOCATOR_REGISTERED.format(service_name=key.__name__))


    @classmethod
    def get(cls, key: type[T]) -> T:
        try:
            return cls.__services[key]
        
        except KeyError:
            raise RuntimeError(f"Service not registered: {key.__name__}")


    @classmethod
    def clear(cls):
        cls.__services.clear()