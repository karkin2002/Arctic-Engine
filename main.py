import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from custom.scripts.menu import Menu

## Arctic Engine Test ---------------
from scripts.game.Tile import StaticTile
from scripts.game.ArcticEngine import ArcticEngine
## ----------------------------------

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
    b_colour="MENU_BACK",
    framerate=9999)

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
menu = Menu()
Menu.set_fps_counter(window)
Menu.set_main_menu(window)
Menu.set_options_menu(window)


## TILE TEST SUITE ----------------------------
glob.add_img_surf("test_texture", pygame.image.load(r"static\images\tile_texture.png"))

test_tile = StaticTile("test_texture")

arc_eng = ArcticEngine()
arc_eng.new_map((2,2), "test_texture")

Menu.add_no_selection(window, "game_scale", "Game Scale", -60, arc_eng.get_game_scale(), align_bottom = True)

arc_eng.set_game_scale(10)
## --------------------------------------------

# Create a pygame surface with transparent background
surface = pygame.Surface((4, 4), pygame.SRCALPHA)

# Draw a red circle on the surface
pygame.draw.circle(surface, (255, 0, 0), (2, 2), 2)



### Main Loop -----------------------------
glob.audio.setVolume(100)

run = True
while run:
    
    run = menu.handle_menus(window, run)

    if not window.events():
        run = False
        
    if glob.get_tag(Menu.MAIN_MENU).display or glob.get_tag(Menu.OPTIONS_MENU).display:
        window.draw()
        
    else:
        if window.is_pressed("game_scale_up", hold=True):
            arc_eng.set_game_scale(arc_eng.get_game_scale() + (0.02 * glob.delta_time))
        
        if window.is_pressed("game_scale_down", hold=True):
            arc_eng.set_game_scale(arc_eng.get_game_scale() - (0.02 * glob.delta_time))
        
        window.draw(
            b_surf=(arc_eng.get_game_surf(window.resized, window.win_dim), (0,0)),
            f_surf=(surface,(window.win_dim[0]/2 - 2, window.win_dim[1]/2 - 2))
        )

pygame.quit()
### -----------------------------------------