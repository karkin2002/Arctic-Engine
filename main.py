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
from scripts.ui.ui import WindowUI
from custom.scripts.menu import Menu

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")  
pygame.init()
glob.init()

## Setting global data.
TITLE = r"static/fonts/title_font.ttf"
REGULAR = r"static/fonts/regular_font.ttf"
BOLD = r"static/fonts/bold_font.ttf"

glob.add_font("title", TITLE, 110)
glob.add_font("sub_title", TITLE, 30)

glob.add_font("menu_button_u", REGULAR, 48)
glob.add_font("menu_button_h", BOLD, 46)
glob.add_font("menu_button_p", REGULAR, 40)
glob.add_font("font", REGULAR, 40)

glob.add_colour("WHITE", (255, 255, 255))
glob.add_colour("BLACK", (0, 0, 0))
glob.add_colour("MENU_BACK", (254, 44, 84))

## Loading window UI.
window = WindowUI(
    (1920 , 1080),
    "Arctic Engine",
    b_colour="MENU_BACK",
    framerate=9999)

## Setting Audio
glob.audio.addCat(Menu.AUDIO_MAIN_MENU)
glob.audio.addAudio(Menu.AUDIO_MAIN_MENU, r"static/audio/music/music.wav")

AUDIO_UI = "ui"
glob.audio.addCat(AUDIO_UI)
glob.audio.addAudio(AUDIO_UI, r"static/audio/sfx/ui/button_1.wav")
glob.audio.addAudio(AUDIO_UI, r"static/audio/sfx/ui/button_2.wav")
glob.audio.addAudio(AUDIO_UI, r"static/audio/sfx/ui/button_3.wav")
glob.audio.addAudio(AUDIO_UI, r"static/audio/sfx/ui/button_4.wav")

## Setting Menus
menu = Menu()
Menu.set_fps_counter(window)
Menu.set_main_menu(window)
Menu.set_options_menu(window)

glob.get_tag("fps").display = False


### Main Loop -----------------------------
glob.audio.setVolume(0)

run_first_time = True

run = True
while run:
    run = menu.handle_menus(window, run)
    
    if not window.events():
        run = False
    
    window.draw()
    
    if run_first_time:
        run_first_time = False

pygame.quit()
### -----------------------------------------