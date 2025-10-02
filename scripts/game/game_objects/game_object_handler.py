from scripts.game.game_objects import game_object
from scripts.utility.logger import Logger
from scripts.game.game_objects.camera.camera import Camera
from scripts.game.game_objects.game_object import GameObject
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.window_service import WindowService


class GameObjectHandler:

    __GAME_OBJECT_REPLACED = "Game Object '{game_object_name}' already exists. {pre_game_object} replaced by {post_game_object}"
    __GAME_OBJECT_ADDED = "Game Object '{game_object_name}' has been added as {game_object}."
    __GAME_OBJECT_DOES_NOT_EXIST = "Game Object '{game_object_name}' does not exist."
    __GAME_OBJECT_REMOVED = "Game Object '{game_object_name}' removed."
    __GAME_OBJECT_COULD_NOT_BE_REMOVED = "Game Object '{game_object_name}' could not be removed, as it doesn't exist."

    __INVALID_CAMERA_TEXT = ("{camera_ident} is not a valid camera. Please ensure the component you are setting as the" +
                             "camera exists as a component and is of type Camera object.")
    __CAMERA_SET_NONE_TEXT = "Camera has been unset."
    __CAMERA_SET_TEXT = "Camera has been set to '{camera_ident}'."

    def __init__(self):

        self.__game_objects: dict[str, GameObject] = {}

        self.__window_service = ServiceLocator.get(WindowService)

        ## Camera
        # Setting camera to the identifier for a Camera object stored in the __game_objects dictionary, applies those
        # camera's modifiers to the screen / __game_objects (e.g. move everything to the left, the center is the center
        # of the window).
        self.__camera = None


    def add(self, name: str, new_game_object: GameObject, safety_check: bool = True):

        if safety_check:
            if new_game_object in self.__game_objects:
                Logger.log_warning(self.__GAME_OBJECT_REPLACED.format(
                    game_object_name = name,
                    pre_game_object = self.__game_objects[name],
                    post_game_object = new_game_object))

            else:
                Logger.log_info(self.__GAME_OBJECT_ADDED.format(game_object_name = name, game_object = new_game_object))

        self.__game_objects[name] = new_game_object



    def get(self, name: str, safety_check: bool = True) -> GameObject | None:

        if not safety_check:
            return self.__game_objects[name]


        elif not Logger.raise_key_error(
                self.__game_objects,
                name,
                self.__GAME_OBJECT_DOES_NOT_EXIST.format(game_object_name = name)):

            return self.__game_objects[name]



    def remove(self, name: str, safety_check: bool = True) -> GameObject | None:

        if not safety_check:
            del self.__game_objects[name]

        elif not Logger.raise_key_error(
                self.__game_objects,
                name,
                self.__GAME_OBJECT_DOES_NOT_EXIST.format(game_object_name = name),
                False):

            del self.__game_objects[name]

            Logger.log_info(self.__GAME_OBJECT_REMOVED.format(game_object_name = name))

        else:
            Logger.log_info(self.__GAME_OBJECT_COULD_NOT_BE_REMOVED.format(game_object_name = name))



    def set_camera(self, camera_ident: str | None):
        """
        Sets the camera to a specified camera component.
        """

        if camera_ident is None:
            self.__camera = camera_ident
            Logger.log_warning(self.__CAMERA_SET_NONE_TEXT)
            return

        elif camera_ident in self.__game_objects:
            if isinstance(self.__game_objects[camera_ident], Camera):
                self.__camera = camera_ident
                Logger.log_info(self.__CAMERA_SET_TEXT.format(camera_ident=camera_ident))
                return

        Logger.log_error(self.__INVALID_CAMERA_TEXT.format(camera_ident=camera_ident))



    def get_camera_ident(self) -> str | None:
        return self.__camera



    def draw_game_objects_to_window(self):

        camera: Camera | None = None
        if self.__camera:
            camera: Camera = self.__game_objects[self.__camera]

        for game_obj_ident, game_obj in self.__game_objects.items():

            if game_obj.display:

                comp_surf = game_obj.draw()

                if comp_surf is not None and game_obj_ident != self.__camera:

                    if camera:
                        draw_pos = camera.world_to_screen(game_obj.move.get_draw_pos(), self.__window_service.center)
                    else:
                        draw_pos = game_obj.move.get_draw_pos() + self.__window_service.center

                    self.__window_service.win.blit(comp_surf, (int(draw_pos.x), int(draw_pos.y)))



    def update(self):
        for comp_ident, comp in self.__game_objects.items():
            comp.update()


