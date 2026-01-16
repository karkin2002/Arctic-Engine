## Sprite is a component that can be added to game object to give them a visible sprite. It handles the management of
## the sprite images and how to display them as well as animations.
from pygame import Surface

from scripts.utility.logger import Logger
from scripts.game.components.animation import Animation
from scripts.services.service_locator import ServiceLocator
from scripts.services.visual.colour_service import ColourService
from scripts.services.visual.image_service import ImageService

class AnimationHandler:

    __ANIMATION_REPLACED = "Animation '{animation_name}' replaced from {pre_animation} to {post_animation}."
    __ADDED_ANIMATION = "Animation '{animation_name}' added as {animation}."
    __REMOVED_ANIMATION = "Animation '{animation_name}' removed."
    __ANIMATION_COULD_NOT_BE_REMOVED = "Animation '{animation_name}' could not be removed as it does not exist."
    __CURRENT_ANIMATION_IS_NONE = "Current animation is set to None. Falling back to default Animation '{animation_name}'."
    __ANIMATION_DOES_NOT_EXIST = "Animation '{animation_name}' does not exist. Animation not set."
    __DEFAULT_ANIMATION_NOT_SET = "Default animation not set. Falling back to Animation '{animation_name}'."

    __default_surface = Surface((20, 20))
    __default_surface.fill(ColourService.ERROR_COLOUR_VALUE)

    def __init__(self):

        self.__animations: dict[str, Animation | str] = {}

        self.__current_animation: str | None = None
        self.__default_animation: str | None = None

        self.__image_service = ServiceLocator.get(ImageService)


    def add(self, name: str, animation: Animation | str):

        if name in self.__animations:
            Logger.log_warning(self.__ANIMATION_REPLACED.format(
                animation_name = name,
                pre_animation = self.__animations[name],
                post_animation = animation))

        else:
            Logger.log_info(self.__ADDED_ANIMATION.format(animation_name = name, animation = animation))

        self.__animations[name] = animation


    def get_list(self) -> list[str]:
        return self.__animations.keys()


    def remove(self, name: str):
        if name in self.__animations:
            del self.__animations[name]
            Logger.log_info(self.__REMOVED_ANIMATION.format(animation_name=name))

        else:
            Logger.log_warning(self.__ANIMATION_COULD_NOT_BE_REMOVED.format(animation_name=name))


    def set_current_animation(self, name: str, animation_reset: bool = False):

        if not Logger.raise_key_error(self.__animations, name, self.__ANIMATION_DOES_NOT_EXIST.format(animation_name=name), False):
            if animation_reset or self.__current_animation != name:
                self.__current_animation = name
                self.__animations[self.__current_animation].reset()


    def get_current_animation_name(self) -> str:
        return self.__current_animation


    def set_default_animation(self, name: str):
        if not Logger.raise_key_error(self.__animations, name, self.__ANIMATION_DOES_NOT_EXIST.format(animation_name=name), False):
            self.__default_animation = name


    def get_default_animation_name(self) -> str:
        return self.__default_animation


    def get_frame(self) -> Surface:

        if self.__current_animation is None:
            Logger.log_error(self.__CURRENT_ANIMATION_IS_NONE.format(animation_name=self.__default_animation))
            self.set_current_animation(self.__default_animation)
            return self.__default_surface


        elif type(self.__animations[self.__current_animation]) is Animation:

            if not self.__animations[self.__current_animation].repeat and self.__animations[self.__current_animation].finished:
                if self.__default_animation:
                    self.set_current_animation(self.__default_animation)
                else:
                    Logger.log_warning(self.__DEFAULT_ANIMATION_NOT_SET.format(animation_name=self.__current_animation))

            return self.__image_service.get(self.__animations[self.__current_animation].get_current_frame()).surface

        else:
            return self.__image_service.get(self.__animations[self.__current_animation]).surface


    def is_current_animation_finished(self) -> bool:
        return self.__animations[self.__current_animation].finished
