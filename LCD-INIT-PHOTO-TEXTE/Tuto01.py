# Importation des librairies propres aux images
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Importation des libraries pour la gestion de l'écran
from lib_tft24T import TFT24T
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import spidev

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



#GESTION PHOTO
fond = Image.open('background.jpg')
fond = fond.rotate(-90,expand=True) #Rotation
fond = fond.resize((240,320))       #Redimensionnement
fond.save('fond.jpg')               #Sauvegarde

logo = Image.open('logo-iut-rennes.png')
logo = logo.rotate(-90,expand=True) #Rotation
logo.save('logo.png')               #Sauvegarde

img1= Image.open('fond.jpg')        #Ouvrir
img2= Image.open('logo.png')        #Ouvrir
img1.paste(img2,(0,0), img2)
img1.save('composition.jpg')
zone_ecran.pasteimage('composition.jpg',(0,0))

#GESTION TEXTE
zone_ecran.rectangle(((5,20),(43,300)),fill=(70,70,70))
police = ImageFont.truetype('polices/KGPrimaryItalics.ttf',36)
zone_ecran.textrotated((8,35),'Département GEII',270, font=police, fill=(255,203,0))

#AFFICHER SUR L'ECRAN
TFT.display()


