__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from pygame import event as pygame_event, VIDEORESIZE, QUIT, key as pygame_key, K_w, K_a, K_s, K_d, Vector2
from scripts.utility.logger import Logger
from scripts.game.components.window import Window
from scripts.game.game_objects.game_object import GameObject
from scripts.services.time_service import Time
from scripts.services.image_service import ImageService
from scripts.services.service_locator import ServiceLocator
from scripts.game.game_objects.camera.camera import Camera
import scripts.utility.glob as glob
glob.init()

class ArcticEngine:

    __START_UP_INFO_TEXT = "Initialising Arctic Engine."

    __INVALID_CAMERA_TEXT = ("{camera_ident} is not a valid camera. Please ensure the component you are setting as the" +
                             "camera exists as a component and is of type Camera object.")
    __CAMERA_SET_NONE_TEXT = "Camera has been unset."
    __CAMERA_SET_TEXT = "Camera has been set to '{camera_ident}'."

    def __init__(self,
                 win_dim: tuple[int, int] = (1280, 720),
                 framerate: int = 0,
                 update_time_ms: float = 20.0,
                 background: str | None = None):

        ## Logging
        Logger.log_info(self.__START_UP_INFO_TEXT)

        ## Window Essentials
        self.window = Window(win_dim, background)
        ServiceLocator.register(Window, self.window)

        ## Setup Image Service
        self.image = ImageService()
        ServiceLocator.register(ImageService, self.image)
        ServiceLocator.register(ImageService, self.image)

        ## Components
        self.game_objects: dict[str, GameObject] = {}

        ## Clock / Framerate
        self.time = Time(framerate, update_time_ms)
        ServiceLocator.register(Time, self.time)

        ## Camera
        # Setting camera to the identifier for a Camera object stored in the game_objects dictionary, applies those
        # camera's modifiers to the screen / game_objects (e.g. move everything to the left, the center is the center
        # of the window).
        self.__camera: str | None = None




    def handle_events(self) -> bool:
        """
        This method handles the engines events, including update, fixed update, and drawing to the screen.

        TO-DO: Other events such as handling the quit button.

        Returns:
            bool: True if the engine is still running, False otherwise.
        """

        glob.update_delta_time()

        for event in pygame_event.get():

            if event.type == VIDEORESIZE:
                self.window.resize()

            if event.type == QUIT:
                return False

        return True


    def update(self):
        """
        Updates all game_objects that have an implemented update function & updates the clock. This method runs every frame.
        """

        ## Updates time
        self.time.tick()

        ## Potentially runs multiple times if there is a large lag, i.e. game is rendering at lower ms than
        ## update_time_ms.
        while self.time.is_update():
            for comp_ident, comp in self.game_objects.items():
                comp.update()

            keys = pygame_key.get_pressed()

            velocity = 200

            move_camera = Vector2(0, 0)

            if keys[K_w]:
                if self.__camera:
                    move_camera.y -= velocity

            if keys[K_a]:
                if self.__camera:
                    move_camera.x -= velocity

            if keys[K_s]:
                if self.__camera:
                    move_camera.y += velocity

            if keys[K_d]:
                if self.__camera:
                    move_camera.x += velocity

            self.game_objects[self.__camera].move.move_pos(move_camera)


    def draw(self):
        """
        Draws all game_objects that have an implemented draw function.
        """

        self.window.draw_background()

        self.__draw_components()

        self.window.draw()


    def __draw_components(self):

        camera: Camera | None = None
        if self.__camera:
            camera: Camera = self.game_objects[self.__camera]

        for game_obj_ident, game_obj in self.game_objects.items():

            comp_surf = game_obj.draw()

            if comp_surf is not None and game_obj_ident != self.__camera:

                if camera:
                    draw_pos = camera.world_to_screen(game_obj.move.get_draw_pos(), self.window.center)
                else:
                    draw_pos = game_obj.move.get_draw_pos() + self.window.center

                self.window.win.blit(comp_surf, (int(draw_pos.x), int(draw_pos.y)))



    def set_camera(self, camera_ident: str | None):
        """
        Sets the camera to a specified camera component.
        """

        if camera_ident is None:
            self.__camera = camera_ident
            Logger.log_warning(self.__CAMERA_SET_NONE_TEXT)
            return

        elif camera_ident in self.game_objects:
            if isinstance(self.game_objects[camera_ident], Camera):
                self.__camera = camera_ident
                Logger.log_info(self.__CAMERA_SET_TEXT.format(camera_ident=camera_ident))
                return

        Logger.log_error(self.__INVALID_CAMERA_TEXT.format(camera_ident=camera_ident))


    def get_camera_ident(self) -> str | None:
        return self.__camera

