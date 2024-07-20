import pygame, scripts.utility.glob as glob
from scripts.utility.glob import Tag
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from scripts.ui.ui_element import Text, Image, Button


## TO-DO:
## - Scaling UI elements. Have a universal scale value. At the lowest level
## possible, scale all dimensions/positioning by this value. Allow user to edit
## value.
## - Recreate the Korean Demo main menu



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

glob.add_colour("BLACK", (0, 0, 0))


## Loading window UI.
window = WindowUI((1920, 1080), caption = "유학생 - Yu-Hak-Saeng")



## Setting Audio
AUDIO_MAIN_MENU = "main_menu"
glob.audio.addCat(AUDIO_MAIN_MENU)
glob.audio.addAudio(AUDIO_MAIN_MENU, r"static\audio\music\music.wav")

AUDIO_UI = "ui"
glob.audio.addCat(AUDIO_UI)
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_1.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_2.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_3.wav")
glob.audio.addAudio(AUDIO_UI, r"static\audio\sfx\ui\button_4.wav")


### MAIN MENU ----------------------------
MAIN_MENU = "main_menu"
glob.add_tag(Tag(MAIN_MENU, "Main menu elements.", True))

window.add_elem("title",
                Text("유학생", "title", "BLACK", 
                     offset = (0, -330),
                     tags = [MAIN_MENU]))

window.add_elem("sub_title",
                Text("Yu-Hak-Saeng", "sub_title", "BLACK", 
                     offset = (0, -230),
                     tags = [MAIN_MENU]))

MENU_BUTTONS = ["Continue", "New Save", "Load Save", "Options", "Quit"]

offset = 0
gap = 90
count = 0
for i in range(len(MENU_BUTTONS)):
    window.add_elem(
        MENU_BUTTONS[i],
        Button(
               Text(MENU_BUTTONS[i], "menu_button_u", "BLACK", 
                    offset=(0, offset + (i * gap)), tags = [MAIN_MENU]),
               Text(MENU_BUTTONS[i], "menu_button_h", "BLACK", 
                    offset=(0, offset + (i * gap)), tags = [MAIN_MENU]),
               Text(MENU_BUTTONS[i], "menu_button_p", "BLACK", 
                    offset=(0, offset + (i * gap)), tags = [MAIN_MENU]),
               ("ui", "button_3"),
               ("ui", "button_1"))
    )
### ------------------------------------------





### Main Loop -----------------------------
glob.audio.play(AUDIO_MAIN_MENU, "music", 99)

run = True
while run:
    
    ## Main menu buttons
    for button_name in MENU_BUTTONS:
        
        if button_name == "Continue" and window.is_pressed(button_name):
            glob.audio.pause(AUDIO_MAIN_MENU, "music")
            glob.get_tag(MAIN_MENU).display = False
        
        elif button_name == "Quit" and window.is_pressed(button_name):
            run = False
        
        else:
            window.is_pressed(button_name)
            

    if not window.events():
        run = False

    window.draw()

pygame.quit()
### -----------------------------------------