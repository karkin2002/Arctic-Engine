import copy

from pygame import Vector2
from scripts.utility.logger import Logger
from scripts.game.components.animation import Animation
from scripts.game.game_objects.particle.particle import Particle
from scripts.services.service_locator import ServiceLocator
from scripts.services.utility.persistent_storage_service import PersistentDataService
from scripts.services.utility.persistent_storage_service import PersistentData
from scripts.services.visual.image_service import ImageService


class ParticleService:

    __CONFIG_NAME = "particles"
    __CONFIG_PATH = f"{PersistentDataService.CONFIG_DIR}/{__CONFIG_NAME}.json"

    __TEXTURE_PATH = "static/images/textures/particle/{particle_name}"
    __TEXTURE_NAME_FORMAT = "{particle_name}{frame_num}"

    __TEXTURE = "texture"
    __FRAMES = "num_frames"
    __DURATION = "duration"

    __FAILED_TO_PARSE_CONFIG = "Failed to parse config '{config_path}' for particle '{particle_name}'."

    def __init__(self):
        self.__particles: dict[str, list] = {}

        self.__persistent_data = ServiceLocator.get(PersistentDataService)
        self.__persistent_data.add(ParticleService.__CONFIG_PATH)

        self.__image_service = ServiceLocator.get(ImageService)

        self.load_config()


    def __parse_config(self, name: str, config_data: PersistentData):
        texture = config_data.get_data(name, ParticleService.__TEXTURE)
        frames = config_data.get_data(name, ParticleService.__FRAMES)
        duration = config_data.get_data(name, ParticleService.__DURATION)

        if texture and frames and duration:
            texture_list = []
            for i in range(frames):
                texture_list.append(ParticleService.__TEXTURE_NAME_FORMAT.format(particle_name=name, frame_num=i+1))

            self.__particles[name] = [texture_list, duration, False]

        else:
            Logger.log_error(ParticleService.__FAILED_TO_PARSE_CONFIG.format(config_path=ParticleService.__CONFIG_PATH, particle_name=name))


    def load_config(self):
        particle_config_data = self.__persistent_data.load(ParticleService.__CONFIG_NAME)

        for particle_name in particle_config_data.data:
            self.__image_service.add_folder(ParticleService.__TEXTURE_PATH.format(particle_name=particle_name))
            self.__parse_config(particle_name, particle_config_data)


    def create_particle(self, name: str, pos: Vector2 = Vector2(0, 0)) -> Particle | None:

        if name in self.__particles:
            new_particle = Particle(Animation(*self.__particles[name]))
            new_particle.move.set_pos(pos)
            return new_particle

        return None

