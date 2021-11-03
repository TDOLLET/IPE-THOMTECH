#TP6 EX1
#LCD 
#Afficher code postal

# Importation des librairies
import requests
import csv

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
import textwrap

# Récupération du fichier officiel des codes postaux s'il n'existe pas
try :
    with open('codes_postaux.csv') :
        pass
except IOError :
    url = 'https://datanova.legroupe.laposte.fr/explore/dataset/laposte_hexasmal/download/?format=csv&timezone=Europe/Berlin&use_labels_for_header=true'
    mon_fichier = requests.get(url)
    with open('codes_postaux.csv', 'wb') as donnees :
        donnees.write(mon_fichier.content)
        
# Demande à l'utilisateur le nom de la commune
commune = input("Saisir le nom de la commune : ")
# Mise en majuscules
commune = commune.upper()
# Affichage du nom de la commune dans la console
print(commune)

# Extraction du code postal dans le fichier CSV
fichier_csv = open("codes_postaux.csv", "r")
try :
    lecteur_csv = csv.reader(fichier_csv, delimiter=";")
    for ligne in lecteur_csv :
        if ligne[1] == commune :
            print(ligne[2])
            code_p = ligne[2]


finally :
    fichier_csv.close()
    
    
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

zone_ecran.rectangle(((0,0),(240,320)),fill=(10,2,87))
police1 = ImageFont.truetype('polices/DK_Pimpernel.otf',36)
police2 = ImageFont.truetype('polices/DK_Pimpernel.otf',65)

zone_ecran.textrotated((180,35),"CODE POSTAL DE",270, font=police1, fill=(255,255,255))
zone_ecran.textrotated((144,50),commune +":",270, font=police1, fill=(255,255,255))
zone_ecran.textrotated((30,35),code_p,270, font=police2, fill=(255,255,255))

TFT.display()


