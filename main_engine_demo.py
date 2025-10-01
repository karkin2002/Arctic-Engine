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
from scripts.game.arctic_engine import ArcticEngine
from scripts.game.game_objects.map.map import Map
from scripts.game.game_objects.camera.camera import Camera
from scripts.game.components.tag_handler import TagHandler, Tag


## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")
pygame.init()

### Setup Game Engine -----------------------------
ae = ArcticEngine()
ae.time.set_stable_framerate(True)

## Map
ae.image.add_image("test_texture_1", pygame.image.load("static/images/tile_texture_1.png"))
ae.image.add_image("test_texture_2", pygame.image.load("static/images/tile_texture_2.png"))
test_map = Map((100, 100))
test_map.add_map_layer()
test_map.get_map_layer(0).generate_map_array(["test_texture_1", "test_texture_2"], [0.2, 0.8])
test_map.set_map_surf()
ae.game_objects["map"] = test_map

## Camera
TagHandler.add_tag(Tag("Camera", "This is a camera"))

test_camera = Camera()
ae.game_objects["default_camera"] = test_camera
ae.set_camera("default_camera")
test_camera.move.set_pos(pygame.Vector2(0, 0))

test_camera.tag.assign_tag("Camera", test_camera)



### Main Loop -----------------------------
run = True
while run:

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------