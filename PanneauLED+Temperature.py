#TP 3 Ex3
#Carte d'extension "Sente Hat"
#Afficher la température de la pièce sur le panneau led
from sense_hat import SenseHat
import random
import time

sense=SenseHat()

while True:
    try:
        temperature=(sense.get_temperature())
        
        sense.set_rotation(180)
        
        if(temperature<25):
            fond=[0,0,255]
            
        elif(temperature>25 and temperature<35):
            fond=[255,0,255]
            
        else:
            fond=[255,0,0]
        
        sense.show_message(str(round(temperature,1)),text_colour=[255,255,0],back_colour=fond)
        time.sleep(0.3)
        
    except KeyboardInterrupt:
        sense.clear()
        print("Au revoir !!!")
        break


