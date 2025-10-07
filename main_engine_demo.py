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

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")
pygame.init()

### Setup Game Engine -----------------------------
ae = ArcticEngine()
ae.time.set_stable_framerate(True)
ae.colour.add_colour("blue", (147, 202, 237))
ae.window.background_colour = "blue"

## Map
ae.image.add("test_texture_1", pygame.image.load("static/images/tile_texture_1.png"))
ae.image.add("test_texture_2", pygame.image.load("static/images/tile_texture_2.png"))
test_map = Map((100, 100))
test_map.add_map_layer()
test_map.get_map_layer(0).generate_map_array(["test_texture_1", "test_texture_2"], [0.2, 0.8])
test_map.set_map_surf()
ae.game_objects.add("map", test_map)

## Test entities
ae.image.add_folder("custom/images/")

test_entity_1 = TestEntity()
ae.game_objects.add("test_entity_1", test_entity_1)

test_entity_2 = TestEntity()
ae.game_objects.add("test_entity_2", test_entity_2)
test_entity_2.move.set_pos(pygame.Vector2(-100, -100))


## Camera
test_camera = Camera()
ae.game_objects.add("default_camera", test_camera)
ae.game_objects.set_camera("default_camera")
test_camera.move.set_pos(pygame.Vector2(0, 0))


## Music
# ae.audio.add_cat("music", 100)
# ae.audio.add_audio("music", "custom/music.wav", volume=100)
# ae.audio.play("music", "music")

### Main Loop -----------------------------
run = True
while run:

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------