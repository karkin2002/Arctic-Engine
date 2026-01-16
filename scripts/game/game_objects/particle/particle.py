from pygame import Surface

from scripts.game.game_objects.game_object import GameObject
from scripts.game.components.animation import Animation
from scripts.game.components.animation_handler import AnimationHandler

class Particle(GameObject):
    PARTICLE_ANIMATION_NAME = "particle_animation"

    def __init__(self, animation: Animation):
        super().__init__()

        self.__animation_handler: AnimationHandler | None = None
        self.__init_animation(animation)

    def __init_animation(self, animation: Animation):
        self.__animation_handler = AnimationHandler()
        self.__animation_handler.add(Particle.PARTICLE_ANIMATION_NAME, animation)
        self.__animation_handler.set_default_animation(Particle.PARTICLE_ANIMATION_NAME)
        self.__animation_handler.set_current_animation(Particle.PARTICLE_ANIMATION_NAME)
        self.move.set_dim(animation.get_dim())

    def draw(self) -> Surface | None:

        return self.__animation_handler.get_frame()