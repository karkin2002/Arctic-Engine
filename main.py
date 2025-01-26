import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from custom.scripts.menu import Menu
from scripts.game.Camera import Camera

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

glob.get_tag("fps").display = False


## TILE TEST SUITE ----------------------------
glob.add_img_surf("test_texture", pygame.image.load(r"static\images\tile_texture.png"))

arc_eng = ArcticEngine()
arc_eng.new_map((20,20), "test_texture")

## --------------------------------------------

surface = pygame.Surface((4, 4), pygame.SRCALPHA)

pygame.draw.circle(surface, (255, 0, 0), (2, 2), 2)

### Main Loop -----------------------------
glob.audio.setVolume(100)

arc_eng.add_camera("test_camera", Camera((0,0), 1))
arc_eng.get_camera("test_camera").set_scale(10)

run = True
while run:
    run = menu.handle_menus(window, run)

    if not window.events():
        run = False
        
    if glob.get_tag(Menu.MAIN_MENU).display or glob.get_tag(Menu.OPTIONS_MENU).display:
        window.draw()
        
    else:
        camera = arc_eng.get_camera("test_camera")
        
        if window.keyboard.is_pressed("camera_up", hold=True):
            camera.move_pos((0, 2))
            
        if window.keyboard.is_pressed("camera_down", hold=True):
            camera.move_pos((0, -2))
            
        if window.keyboard.is_pressed("camera_right", hold=True):
            camera.move_pos((-2, 0))
            
        if window.keyboard.is_pressed("camera_left", hold=True):
            camera.move_pos((2, 0))
        
        if window.keyboard.is_pressed("zoom_in", hold=True):
            camera.adjust_scale(0.2)
        
        if window.keyboard.is_pressed("zoom_out", hold=True):
            camera.adjust_scale(-0.2)


        arc_eng.set_game_surf(window.resized, window.win_dim, "test_camera")

        
        window.draw(
            b_surf=(arc_eng.game_surf, arc_eng.game_surf_pos),
            f_surf=(surface,(window.win_dim[0]/2 - 2, window.win_dim[1]/2 - 2))
        )

pygame.quit()
### -----------------------------------------