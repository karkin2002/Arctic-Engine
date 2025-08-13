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

import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.game.arctic_engine import ArcticEngine
from scripts.game.components.map.Map import Map
from scripts.game.components.camera.camera import Camera


## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")  
pygame.init()
glob.init()

### Setup Game Engine -----------------------------
glob.add_colour("red", (200,100,100))
ae = ArcticEngine(background="red", framerate=60, update_time_ms=20)

## Map
glob.add_img_surf("test_texture_1", pygame.image.load("static/images/tile_texture_1.png"))
glob.add_img_surf("test_texture_2", pygame.image.load("static/images/tile_texture_2.png"))
test_map = Map((100, 100))
test_map.add_map_layer()
test_map.get_map_layer(0).generate_map_array(["test_texture_1", "test_texture_2"], [0.2, 0.8])
test_map.set_map_surf()
ae.components["map"] = test_map

## Camera
test_camera = Camera((0, 0))
ae.components["camera"] = test_camera
ae.set_camera("camera")


### Main Loop -----------------------------
run = True
while run:

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------