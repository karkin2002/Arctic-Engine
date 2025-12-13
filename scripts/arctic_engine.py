__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

from scripts.game.game_objects.entity.test_entity import TestEntity

"""
This file is part of Arctic Engine Project by Kaya Arkin. For more information,
look at the README.md file in the root directory, or visit the
GitHub Repo: https://github.com/karkin2002/Arctic-Engine.
"""

from pygame import event as pygame_event, VIDEORESIZE, QUIT, key as pygame_key, K_w, K_a, K_s, K_d, K_SPACE, Vector2
from scripts.utility.logger import Logger
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.window_service import WindowService
from scripts.services.utility.time_service import TimeService
from scripts.services.visual.image_service import ImageService
from scripts.services.visual.colour_service import ColourService
from scripts.services.audio.audio_service import AudioService
from scripts.game.game_objects.game_object_handler import GameObjectHandler
import scripts.utility.glob as glob
glob.init()

class ArcticEngine:

    __START_UP_INFO_TEXT = "Initialising Arctic Engine."


    def __init__(self,
                 win_dim: tuple[int, int] = (1280, 720),
                 framerate: int = 0,
                 update_time_ms: float = 20.0,
                 temp_image_lifespan: int = 600000):

        ## Logging
        Logger.log_info(self.__START_UP_INFO_TEXT)

        ## Setup Colour Service
        self.colour = ColourService()
        ServiceLocator.register(ColourService, self.colour)

        ## WindowService Essentials
        self.window = WindowService(win_dim)
        ServiceLocator.register(WindowService, self.window)

        ## Audio Service
        self.audio = AudioService(80)
        ServiceLocator.register(AudioService, self.audio)

        ## Setup Image Service
        self.image = ImageService(temp_image_lifespan)
        ServiceLocator.register(ImageService, self.image)

        ## Game Objects
        self.game_objects = GameObjectHandler()

        ## Clock / Framerate
        self.time = TimeService(framerate, update_time_ms)
        ServiceLocator.register(TimeService, self.time)



    def handle_events(self) -> bool:
        """
        This method handles the engines events, including update, fixed update, and drawing to the screen.

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
        Updates all __game_objects that have an implemented update function & updates the clock. This method runs every frame.
        """

        ## Updates time
        self.time.tick()


        ## Potentially runs multiple times if there is a large lag, i.e. game is rendering at lower ms than
        ## update_time_ms.
        while self.time.is_update():
            self.game_objects.update()

            keys = pygame_key.get_pressed()

            velocity = 200

            move_camera = Vector2(0, 0)

            entity: TestEntity = self.game_objects.get("test_entity_1", False)

            if keys[K_w]:
                    move_camera.y -= velocity
                    entity.animation.set_current_animation("up")

            if keys[K_a]:
                    move_camera.x -= velocity
                    entity.animation.set_current_animation("left")

            if keys[K_s]:
                    move_camera.y += velocity
                    entity.animation.set_current_animation("down")

            if keys[K_d]:
                    move_camera.x += velocity
                    entity.animation.set_current_animation("right")

            if not keys[K_w] and not keys[K_a] and not keys[K_s] and not keys[K_d]:
                entity.animation.set_current_animation("idle")

            if keys[K_SPACE]:
                entity.animation.set_current_animation("animation_test")

            self.game_objects.get(self.game_objects.get_camera_ident(), False).move.move_pos(move_camera)
            entity.move.move_pos(move_camera)




    def draw(self):
        """
        Draws all __game_objects that have an implemented draw function.
        """

        self.window.draw_background()

        self.game_objects.draw_game_objects_to_window()

        self.window.draw()


