import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from scripts.game.menu import Menu

## Loading Logger and initialising.
Logger("logs/UI_Organisation")  
pygame.init()
glob.init()


## Setting global data.
KOREAN_TITLE = r"static\fonts\korean_title.ttf"
KOREAN_REGULAR = r"static\fonts\korean_regular.ttf"
KOREAN_BOLD = r"static\fonts\korean_bold.ttf"

glob.add_font("title", KOREAN_TITLE, 120)
glob.add_font("sub_title", KOREAN_TITLE, 30)

glob.add_font("menu_button_u", KOREAN_REGULAR, 48)
glob.add_font("menu_button_h", KOREAN_BOLD, 46)
glob.add_font("menu_button_p", KOREAN_REGULAR, 40)

glob.add_font("font", "calibri", 40)

glob.add_colour("WHITE", (255, 255, 255))
glob.add_colour("BLACK", (0, 0, 0))
glob.add_colour("MENU_BACK", (254, 44, 84))

## Loading window UI.
window = WindowUI(
    (1920, 1080), 
    "유학생 - Yu-Hak-Saeng",
    b_colour="MENU_BACK")

## Setting Audio
glob.audio.addCat(Menu.AUDIO_MAIN_MENU)
glob.audio.addAudio(Menu.AUDIO_MAIN_MENU, r"static\audio\music\music.wav")

AUDIO_UI = "ui"
glob.audio.addCat(AUDIO_UI)
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_1.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_2.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_3.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_4.wav")

## Setting Menus
Menu.set_main_menu(window)
Menu.set_options_menu(window)

### Main Loop -----------------------------
glob.audio.setVolume(50)
window.set_scale(1)

run = True
while run:
    
    run = Menu.handle_menus(window, run)

    if not window.events():
        run = False

    window.draw()

pygame.quit()
### -----------------------------------------