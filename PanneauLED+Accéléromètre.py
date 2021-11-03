#TP 3 Ex3
#Carte d'extension "Sente Hat"
#Afficher état de accéléromètre sur le panneau led

from sense_hat import SenseHat
import random
import time

plage=[-0.375,-0.225,-0.075,0.075,0.225,0.375]

sense=SenseHat()
sense.set_imu_config(False, True, False)

while True:
    try:
        
        accel=sense.get_accelerometer_raw()
        x=accel.get("x")
        y=accel.get("y")
        
        print("x = {0}, y = {1}".format(round(x,2),round(y,2)))
        
        time.sleep(0.3)
        
        for i in range(0,7):
            sense.set_pixel(0, i, 255, 255, 255)
            sense.set_pixel(7, i, 255, 255, 255)
            sense.set_pixel(i, 7, 255, 255, 255)
            sense.set_pixel(i, 0, 255, 255, 255)
            
        while (i>0
            if(plage[i]>x and plage[i+1]<x)
                
        
    except KeyboardInterrupt:
        sense.clear()
        print("Au revoir !!!")
        break

