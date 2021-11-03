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

# Affichage en boucle des images sur le LCD
# -----------------------------------------
 

while True:
    try :
        for i in range (NB_IMG):
            zone_ecran.pasteimage('bing_search/'+str(mots_clefs)+"/Image_"+str(i+1)+'.jpg',(0,0))
            TFT.display()
            time.sleep(2)
            TFT.clear((0,0,0))
        
    except KeyboardInterrupt:
        # Efface l'écran
        TFT.clear((0,0,0))
        # Supprime le répertoire des images téléchargées
        shutil.rmtree('bing_search/'+ mots_clefs +'/')
