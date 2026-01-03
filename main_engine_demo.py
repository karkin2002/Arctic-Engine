__author__ = "Kaya Arkin"
__copyright__ = "Copyright Kaya Arkin"
__license__ = "GPL"
__email__ = "karkin2002@gmail.com"
__status__ = "Development"

from scripts.game.components.tag_handler import TagHandler

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
from scripts.game.components.tag_handler import TagHandler, Tag

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

TagHandler.add_tag(Tag("game_data"))
TagHandler.add_tag(Tag("settings_data"))

ae.persistent_data.add("custom/save_data/game_data_1.json").tags.assign_tag("game_data", "game_data_1")
ae.persistent_data.add("custom/save_data/game_data_2.json").tags.assign_tag("game_data", "game_data_2")

ae.persistent_data.add("custom/save_data/settings_data.json").tags.assign_tag("settings_data", "settings_data_1")

ae.persistent_data.save_all("settings_data")





ae.persistent_data.get("game_data_1").data = {"Hello": 1}
ae.persistent_data.save("game_data_1")

## Music
# ae.audio.add_cat("music", 100)
# ae.audio.add_audio("music", "static/audio/music/music.wav", volume=100)
# ae.audio.play("music", "music")


### Main Loop -----------------------------
run = True
while run:

    run = ae.handle_events()

    ae.update()

    ae.draw()

pygame.quit()
### -----------------------------------------