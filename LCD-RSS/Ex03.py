#TP6 EX3
#LCD 
#Afficher cinéma

# Importation des librairies
import os
# sudo pip3 install feedparser
import feedparser
import shutil
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time


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

#ecran chargement
img1= Image.open('Allocine.jpg')
img1 = img1.rotate(-90,expand=True)
img1.save('Allocine_1.jpg')
zone_ecran.pasteimage('Allocine_1.jpg',(0,0))

police = ImageFont.truetype('polices/DK_Pimpernel.otf',36)
zone_ecran.textrotated((50,70),"Films de la semaine",270, font=police, fill=(0,0,0))

TFT.display()

#création du dossier affiche
chemin=os.getcwd()+'/affiches/'
if os.path.isdir(chemin)==False:
    os.mkdir('affiches')

# Récupération du flux allocine des sorties de la semaine
url = 'http://rss.allocine.fr/ac/cine/cettesemaine'
flux = feedparser.parse(url)
#print(flux)

# Extraction des informations
entrees_flux = flux.entries
titres_films = []
affiches_films = []
index = 0
for entree in entrees_flux :
    #print (entree.title)
    titres_films.append(entree.title)
    #print(entree/links[1]['href'])
    affiches_films.append(entree.links[1]['href'])
    affiche_fichier = requests.get(affiches_films[index],stream = True)
    fichier =open ("affiches/" + str (index)+ ".jpg",'wb')
    affiche_fichier.raw.decode_content = True
    shutil.copyfileobj(affiche_fichier.raw, fichier)
    fichier.close()
    affiche = Image.open('affiches/' + str(index) + '.jpg')
    affiche = affiche.rotate(-90,expand = True)
    affiche.thumbnail((190,190))
    affiche.save('affiches/' + str(index) + '.jpg')
    index = index + 1
    
print("Ok")
    
while True:
    try :
        police = ImageFont.truetype('polices/DK_Pimpernel.otf',25)
        for i in range (len(titres_films)) :
            TFT.clear((0,0,0))
            zone_ecran.pasteimage('affiches/'+str(i)+'.jpg',(0,96))
            
            titre = textwrap.wrap(titres_films[i], width=40)
            for j in range(0 , len(titre)):
                zone_ecran.textrotated(((190-30*j),40),titre[j],270, font=police, fill=(255,255,255))
            
            #zone_ecran.textrotated((25,20),str(titres_films[i]),270, font=police, fill=(255,255,255))
            
            TFT.display()
            time.sleep(2)
        
    except KeyboardInterrupt:
        break

