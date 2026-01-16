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

import pygame
from scripts.utility.logger import Logger
from scripts.arctic_engine import ArcticEngine
from scripts.game.game_objects.map.map import Map
from scripts.game.game_objects.camera.camera import Camera
from scripts.game.game_objects.entity.test_entity import TestEntity
from scripts.game.game_objects.particle.particle import Particle
from scripts.game.components.animation import Animation
from scripts.game.components.animation_handler import AnimationHandler

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")
pygame.init()

### Setup Game Engine -----------------------------
ae = ArcticEngine()
ae.time.set_stable_framerate(True)
ae.colour.add_colour("blue", (147, 202, 237))
ae.window.background_colour = "blue"


## Load images
ae.image.add_folder("static/images/textures/test_entity/")
ae.image.add_folder("static/images/textures/map/")
ae.image.add_folder("static/images/textures/particle/")

## Map
test_map = Map((100, 100))
test_map.add_map_layer()
test_map.get_map_layer(0).generate_map_array(["test_texture_1", "test_texture_2"], [0.1, 0.9])
test_map.set_map_surf()
test_map.draw_order = 0
ae.game_objects.add("map", test_map)

## Test entities
test_entity_1 = TestEntity()
test_entity_1.draw_order = 1
ae.game_objects.add("test_entity_1", test_entity_1)

## Camera
test_camera = Camera()
ae.game_objects.add("default_camera", test_camera)
ae.game_objects.set_camera("default_camera")
test_camera.move.set_pos(pygame.Vector2(0, 0))

## Music
# ae.audio.add_cat("music", 100)
# ae.audio.add_audio("music", "static/audio/music/music.wav", volume=100)
# ae.audio.play("music", "music")

## Particle
animation = Animation(["explosion1", "explosion2", "explosion3", "explosion4", "explosion5", "explosion6", "explosion7", "explosion8", "explosion9", "explosion10"], 2000, False)
test_particle = Particle(animation)
ae.game_objects.add("test_particle", test_particle)


### Main Loop -----------------------------
run = True
while run:

    print(ae.game_objects.get_game_obj_count())

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------