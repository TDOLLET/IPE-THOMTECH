#Ex4
# Importation des librairies
import os
import shutil
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
# git clone https://github.com/gurugaurav/bing_image_downloader
# sudo python3 setup.py install
# Lien vers doc API : pypi.org/project/bing-image-downloader
from bing_image_downloader import downloader
# Importation des librairies utiles
from ColorCube import ColorCube
from PIL import Image

import board
import neopixel
from time import sleep
from random import randint

# Déclaration du nombre de LEDs à piloter
NOMBRE_LEDS = 2

# Instanciation de l'objet LED
LED_NEOPIXEL = neopixel.NeoPixel(board.D18, NOMBRE_LEDS)


# Importation des libraries pour la gestion de l'écran
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import spidev
import textwrap

# Déclaration des numéros de broches utiles pour la gestion de l'écran
DC = 22
RST = 25
LED = 23

# Instanciation de l'objet LCD
TFT = TFT24T(spidev.SpiDev(), GPIO, landscape=False)

# Initialisation de l'écran
TFT.initLCD(DC, RST, LED)

# Création d'un buffer représentant la zone d'affichage de l'écran
zone_ecran = TFT.draw()
TFT.clear((0,0,0))

# Nombre d'images à télécharger
NB_IMG = 8

# Creation du dossier 'bing_search' s'il n'existe pas
if not os.path.exists("bing_search") :
    os.makedirs("bing_search")

# Demande des mots clefs à l'utilisateur
mots_clefs = input("Quels mots clefs souhaitez-vous pour votre recherche ? ")

# Récupération des images du résultat de la recherche
downloader.download(mots_clefs,limit=NB_IMG,output_dir="bing_search",force_replace=True)

# Création d'une liste qui contiendra le chemin de chaque image téléchargée
liste_fichiers_image=[]

# transformation des images pour les mettre au format de l'écran LCD
for fichier in os.listdir('bing_search/'+ mots_clefs +'/') :
	# On ouvre une image du dossier 'bing_search'
    resultat = Image.open('bing_search/'+ mots_clefs +'/'+fichier)
	# On la tourne de 90° pour l'écran LCD
    resultat = resultat.rotate(-90, expand = True)
	# On la redimensionne en testant si l'image est en portrait ou en paysage
    if resultat.size[0] >= resultat.size[1] :
        resultat.thumbnail((220,220))
    else :
        resultat.thumbnail((300,300))
	# On sauvegarde l'image transformée en écrasant le fichier original
    resultat.save('bing_search/'+ mots_clefs +'/'+fichier)
	# On complète la liste des chemins des différentes images téléchargées
    liste_fichiers_image.append('bing_search/'+ mots_clefs +'/'+fichier)

# importation des librairies utiles
import apds9960 as GestureSensor
from apds9960_constants import *
from gpiozero import DigitalInputDevice  

# Broche d'interruption du capteur APDS-9960
SENSOR_INTERRUPT = 4
cc = ColorCube(avoid_color=[255, 255, 255])

# Fonction d'interruption permettant de lire le geste qui s'est produit
def Lecture_geste():
    i=1
    while(True):
        while capteur_APDS9960.isGestureAvailable():
            geste=capteur_APDS9960.readGesture()
            if geste == Directions.DIR_LEFT:
                    print ("\n\nGauche")
                    if (i>1):
                        i=i-1
            if geste == Directions.DIR_RIGHT:
                    print ("\n\nDroit")
                    if (i<8):
                        i=i+1
            capteur_APDS9960.enableGestureSensor(True)
            TFT.clear((0,0,0))    
            zone_ecran.pasteimage('bing_search/'+str(mots_clefs)+"/Image_"+str(i)+'.jpg',(0,0))
            
            # Instanciation de l'objet color cube, en précisant d'éliminer les couleurs trop proches du blanc
            

            # Chargement d'une image et redimensionnement à la taille (100,100) pour
            # rendre le temps de traitement plus rapide
            # En diminuant la taille, on itensifie aussi la perception des couleurs dominantes
            image = Image.open('bing_search/'+str(mots_clefs)+"/Image_"+str(i)+'.jpg').resize((100,100))

            # Traitement de l'image et extraction des couleurs
            colors = cc.get_colors(image)
            zone_ecran.rectangle(((0,0),(240,320)),fill=(colors[0][0],colors[0][1],colors[0][2]))
            zone_ecran.pasteimage('bing_search/'+str(mots_clefs)+"/Image_"+str(i)+'.jpg',(0,0))
            # Affichage des composantes de la couleur dominante
            LED_NEOPIXEL[0] = (colors[0][0],colors[0][1],colors[0][2])
            LED_NEOPIXEL[1] = (colors[0][0],colors[0][1],colors[0][2])
            
            print ("couleur dominante R : {}".format(colors[0][0]))
            print ("couleur dominante G : {}".format(colors[0][1]))
            print ("couleur dominante B : {}".format(colors[0][2]))
            TFT.display()

# Déclaration de la broche d'interruption du capteur APDS-9960
APDS9960_INT = DigitalInputDevice(SENSOR_INTERRUPT, pull_up = True)
# Précise que lorsqu'un nouveau geste sera détecté (broche d'interruption changera d'état)
# alors on exécutera la fonction 'Lecture_geste()'
APDS9960_INT.when_activated = Lecture_geste

# Déclaration de l'objet associé au capteur APDS-9960
capteur_APDS9960 = GestureSensor.APDS9960(bus=1)
# Initialisation du capteur APDS-9960
capteur_APDS9960.initDevice()
capteur_APDS9960.resetGestureParameters()
# Modification légère des paramètres pour s'adapter au module présent sur la carte (meilleurs résultats de détection)
capteur_APDS9960.setGestureGain(GGAIN_2X)
capteur_APDS9960.setGestureLEDDrive(LED_DRIVE_25MA)
# Rend le capteur APDS-9960 actif  
capteur_APDS9960.enableGestureSensor(True)

# Affichage en boucle des images sur le LCD
# -----------------------------------------

while True:
    try :
        pass
                
    except KeyboardInterrupt:
        # Efface l'écran
        TFT.clear((0,0,0))
        # Supprime le répertoire des images téléchargées
        shutil.rmtree('bing_search/'+ mots_clefs +'/')


