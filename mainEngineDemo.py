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
from scripts.game.ArcticEngine import ArcticEngine

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")  
pygame.init()
glob.init()

### Main Loop -----------------------------
ae = ArcticEngine()

run = True
while run:
    ae.handle_events()

pygame.quit()
### -----------------------------------------