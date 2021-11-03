#TP6 EX1
#LCD 
#Afficher pensée du jour

from bs4 import BeautifulSoup
import requests

URL_site = 'https://www.lapenseedujour.net'

# Récupération de la page
contenu_brut = requests.get(URL_site)
# Trie le contenu html pour le stocker
code_html = BeautifulSoup(contenu_brut.text, 'html.parser')
#print(code_html)

information_recherchee = code_html.find('table', attrs={"class":u"cadre"}).find('font')

# extraction du texte
pensee = information_recherchee.text

print(pensee)

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
police = ImageFont.truetype('polices/Always_In_My_Heart.ttf',28)
pensee = textwrap.wrap(pensee, width=30)
for i in range(0 , len(pensee)):
    zone_ecran.textrotated(((180-20*i),35),pensee[i],270, font=police, fill=(0,0,0))

police = ImageFont.truetype('polices/Simplicity.ttf',36)
zone_ecran.textrotated((8,35),"Pensee du jour",270, font=police, fill=(27,40,137))

TFT.display()


