# Importation des librairies
import requests
import pprint

# www.open-notify.org
# Récupération d'un fichier JSON correspondant au nombre de personne dans l'ISS
url = 'https://data.explore.star.fr/explore/dataset/vls-stations-etat-tr/download/?format=json&timezone=Europe/Berlin&lang=fr'
velo = requests.get(url)


# Récupération de flux JSON au sein de la requête effectuée et affichage
velo_JSON = velo.json()
# print ("FICHIER JSON : ")
# print (velo_JSON)
# print (" ")
# pprint.pprint(velo_JSON)

nom='vide'
while(nom=='vide'):
    station_demande=input("Saisir une station : ")
    for mot in velo_JSON:
        if((mot['fields']['nom']==station_demande)):
            nom=mot['fields']['nom']
            potentiel=mot['fields']['nombreemplacementsactuels']
            dispo=mot['fields']['nombrevelosdisponibles']
            update=mot['fields']['lastupdate']

    if((nom)=='vide'):
           print("Station de vélo introuvable !")

    
#Partie Affichage
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

zone_ecran.rectangle(((0,0),(240,320)),fill=(255,255,255))

img1= Image.open('Logo_STAR_Rennes.jpg')
img1 = img1.rotate(-90,expand=True)
img1.save('logo.jpg')
zone_ecran.pasteimage('logo.jpg',(0,0))

img2= Image.open('Velo_Rennes.jpg')
img2 = img2.rotate(-90,expand=True)
img2.save('Velo.jpg')
zone_ecran.pasteimage('Velo.jpg',(150,220))

police = ImageFont.truetype('polices/Letters_for_Learners.ttf',24)
zone_ecran.textrotated((130,180),nom,270, font=police, fill=(0,0,0))

police = ImageFont.truetype('polices/Letters_for_Learners.ttf',36)
zone_ecran.textrotated((80,200),(str(dispo)+" vélos"),270, font=police, fill=(0,0,0))

police = ImageFont.truetype('polices/Letters_for_Learners.ttf',16)
zone_ecran.textrotated((5,170),str(update),270, font=police, fill=(0,0,0))

TFT.display()



