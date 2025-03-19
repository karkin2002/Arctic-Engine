import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from custom.scripts.menu import Menu
from scripts.game.Camera import Camera
from scripts.game.Map import Map
from scripts.ui.ui_element import Image, Box, TextBox

## Arctic Engine Test ---------------
from scripts.game.Tile import StaticTile
from scripts.game.ArcticEngine import ArcticEngine
## ----------------------------------

## Loading Logger and initialising.
Logger(r"logs/UI_Organisation")  
pygame.init()
glob.init()

## Setting global data.
TITLE = r"static\fonts\korean_title.ttf"
REGULAR = r"static\fonts\korean_regular.ttf"
BOLD = r"static\fonts\korean_bold.ttf"

glob.add_font("title", TITLE, 110)
glob.add_font("sub_title", TITLE, 30)

glob.add_font("menu_button_u", REGULAR, 48)
glob.add_font("menu_button_h", BOLD, 46)
glob.add_font("menu_button_p", REGULAR, 40)
glob.add_font("font", "calibri", 40)

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


def set_dim_based_on_win_dim(run_first_time, window, ui_element, box_dim, dynamic_width = False, dynamic_height = False):
    
    if window.resized or window.rescaled or run_first_time:
        
        if dynamic_width:
            width = (window.win_dim[0] - ((box_dim[0]*glob.scale)*2)) / glob.scale
        else:
            width = box_dim[0]
        
        if dynamic_height:
            height = (window.win_dim[1] - ((box_dim[1]*glob.scale)*2)) / glob.scale
        else:
            height = box_dim[1]
        
        if width < 0:
            width = 0
        if height < 0:
            height = 0
        
        ui_element.box_dim = (width, height)
        
        ui_element.set_surf(window.win_dim)

window.add_elem("text_box_1", 
                TextBox(
                (0, 0), 
                "WHITE", 
                "This is text box 1", 
                "menu_button_u",
                "BLACK",
                (50, 50),
                centered=False,
                align_left = True,
                align_top = True))
text_box_1 = window.get_elem("text_box_1")

window.add_elem("text_box_2", 
                TextBox(
                (0, 0), 
                "WHITE", 
                "This is text box 2", 
                "menu_button_u",
                "BLACK",
                (50, 600),
                centered=False,
                align_left = True,
                align_top = True))
text_box_2 = window.get_elem("text_box_2")


### Main Loop -----------------------------
glob.audio.setVolume(0)

run_first_time = True

run = True
while run:
    run = menu.handle_menus(window, run)
    
    if not window.events():
        run = False
        
    set_dim_based_on_win_dim(run_first_time, window, text_box_1, (50, 300), dynamic_width=True)
    set_dim_based_on_win_dim(run_first_time, window, text_box_2, (50, 300), dynamic_width=True)
        
    if window.is_pressed("text_box_1"):
        window.input_stream.set_input_stream(text_box_1)
    
    elif window.is_pressed("text_box_2"):
        window.input_stream.set_input_stream(text_box_2)
    
    window.draw()
    
    if run_first_time:
        run_first_time = False

pygame.quit()
### -----------------------------------------