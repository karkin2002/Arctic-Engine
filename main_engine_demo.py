__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

from scripts.game.components.filters.low_pass_filter import LowPassFilter

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
from scripts.game.game_objects.entity.square import Square

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")
Logger.print_log = False
pygame.init()

### Setup Game Engine -----------------------------
ae = ArcticEngine(win_dim = (1024, 576), flags=(pygame.SCALED | pygame.FULLSCREEN))
ae.time.set_stable_framerate(True)
ae.colour.add_colour("rich_black", (1, 11, 19))
ae.window.background_colour = "rich_black"

## Load images
ae.image.add_folder("static/images/textures/entity/square/")
ae.image.add_folder("static/images/textures/map/")

## Map
test_map = Map((10, 10))
test_map.add_map_layer()
test_map.get_map_layer(0).generate_map_array(["simple_tile"], [1])
test_map.set_map_surf()
test_map.draw_order = 0
ae.game_objects.add("map", test_map)

## Entities
square1 = Square()
square1.draw_order = 2
ae.game_objects.add("square1", square1)

## Camera
test_camera = Camera()
ae.game_objects.add("default_camera", test_camera)
ae.game_objects.set_camera("default_camera")
test_camera.move.set_pos(pygame.Vector2(0, 0))
test_camera.move.movement_filter = LowPassFilter(0.02, test_camera.move.get_pos())

### Main Loop -----------------------------
run = True
while run:

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------