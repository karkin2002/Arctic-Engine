import pygame, scripts.globvar as globvar
from scripts.logger import Logger
from scripts.ui import WindowUI
from scripts.ui_element import Text, Image, Button


## Loading Logger and initialising.
Logger("logs/UI_Organisation")  
pygame.init()
globvar.init()



## Loading global items.
globvar.add_font("title_font", "verdana", 90)
globvar.add_font("button_up_font", "verdana", 60)
globvar.add_font("button_h_font", "verdana", 65)
globvar.add_font("button_p_font", "verdana", 60)
globvar.add_colour("BLACK", (0, 0, 0))

red_surf = pygame.Surface((200, 200))
red_surf.fill((200, 100, 100))
globvar.add_img_surf("red_sqr", red_surf)

green_surf = pygame.Surface((200, 200))
green_surf.fill((100, 200, 100))
globvar.add_img_surf("green_sqr", green_surf)

globvar.add_img_surf("back_img", pygame.image.load("background.png"))



## Loading window UI.
window = WindowUI((1920, 1080))

window.add_elem("BACK_IMG",
                Image("back_img", 1))

window.add_elem("title",
                Text("Ark Survival",
                     "title_font", 
                     "BLACK", 
                     offset = (0, 70),
                     align_top = True))

text = ["Continue", "Load Save", "Settings", "Exit"]

start = 80
gap = 150
y_offset = -((len(text)/2)*gap) + start
for button_text in text:
    
    p_text = Text(button_text, "button_p_font", "BLACK", (35, y_offset), centered=False, align_left = True) 
    h_text = Text(button_text, "button_h_font", "BLACK", (35, y_offset), centered=False, align_left = True)
    u_text = Text(button_text, "button_up_font", "BLACK", (35, y_offset), centered=False, align_left = True)  
    
    window.add_elem(button_text, Button(u_text, 
                                        hover_elem=h_text, 
                                        press_elem=p_text, 
                                        display=True))
    
    y_offset += gap



## Main Loop.
run = True
while run:
    
    for button_text in text:
        window.is_pressed(button_text)

    if not window.events():
        run = False

    window.draw()

pygame.quit()