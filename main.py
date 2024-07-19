import time
import pygame, scripts.utility.glob as glob
from scripts.utility.logger import Logger
from scripts.ui.ui import WindowUI
from scripts.ui.ui_element import Text, Image, Button
from scripts.audio.audio import UIAudio



## Loading Logger and initialising.
Logger("logs/UI_Organisation")  
pygame.init()
glob.init()


## Loading global items.
glob.add_font("title_font", "calibri", 90)
glob.add_font("button_up_font", "calibri", 60)
glob.add_font("button_h_font", "calibri", 65)
glob.add_font("button_p_font", "calibri", 60)
glob.add_colour("BLACK", (0, 0, 0))



## Loading window UI.
window = WindowUI((1920, 1080))

window.add_elem("title",
                Text("PA Audio Testing Env",
                     "title_font", 
                     "BLACK", 
                     offset = (0, 70),
                     align_top = True))


on_text = Text( "Currently: Playing", "button_up_font", "BLACK", centered=True)
off_text = Text("Currently: Paused", "button_up_font", "BLACK", centered=True)

window.add_elem(
    "toggle_button",
    Button(
        off_text,
        None,
        on_text,
        defualt_toggle_state=True
    )
)


### AUDIO TESTING ------------

audio_test = UIAudio(100)
audio_test.addCat("Home")
audio_test.addAudio("Home", "music.wav")
audio_test.play("Home", "music", 99)
playing = True

### --------------------------






## Main Loop.
run = True
while run:
    
    if window.is_pressed("toggle_button", toggle = True):
        if not playing:
            audio_test.unpause("Home", "music")
            playing = True
    
    else:
        if playing:
            audio_test.pause("Home", "music")
            playing = False
        
            

    if not window.events():
        run = False

    window.draw()

pygame.quit()