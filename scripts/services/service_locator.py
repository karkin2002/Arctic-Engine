from typing import TypeVar
from scripts.utility.logger import Logger

T = TypeVar("T")

class ServiceLocator:

    __NEW_SERVICE_LOCATOR_REGISTERED = "New service locator registered with the class {service_name}."
    __SERVICE_LOCATOR_ALREADY_EXISTS = "Service locator already registered with class {service_name}."
    __SERVICE_NOT_REGISTERED = "Service not registered with class {service_name}."

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
            Logger.raise_exception(ServiceLocator.__SERVICE_NOT_REGISTERED.format(service_name=key.__name__))


    @classmethod
    def clear(cls):
        cls.__services.clear()