# importation des librairies utiles
import apds9960 as GestureSensor
from apds9960_constants import *
from gpiozero import DigitalInputDevice  

# Broche d'interruption du capteur APDS-9960
SENSOR_INTERRUPT = 4

# Fonction d'interruption permettant de lire le geste qui s'est produit
def Lecture_geste():
    while capteur_APDS9960.isGestureAvailable():
        geste=capteur_APDS9960.readGesture()
        if geste == Directions.DIR_NONE:
            print ("Aucun")
        if geste == Directions.DIR_LEFT:
            print ("Gauche")
        if geste == Directions.DIR_RIGHT:
            print ("Droit")
        if geste == Directions.DIR_UP:
            print ("Haut")
        if geste == Directions.DIR_DOWN:
            print ("Bas")
        if geste == Directions.DIR_NEAR:
            print ("Proche")
        if geste == Directions.DIR_FAR:
            print ("Loin")
        capteur_APDS9960.enableGestureSensor(True)

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

# Boucle infinie d'attente d'interruption
try:
    while True:
        pass
except KeyboardInterrupt:
    capteur_APDS9960.resetGestureParameters()
    print ("STOP")
