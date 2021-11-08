# importation des librairies utiles
import RPi.GPIO as GPIO
import BMP280
import time

# initialisation du module Rpi.GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

BMP280.init()


try :
    # création d'un objet basé sur la classe BMP280
    capteur_bmp280 = BMP280.BMP280()
    # initialisation du capteur
    capteur_bmp280.init()
    # Lecture de la température (valeur entière)
    temp_bmp280 = BMP280.temperature()
    # lecture de la pression (valeur entière)
    pression_bmp280 = BMP280.pressure()
    # affichage dans la console des valeurs obtenues
    print(round(temp_bmp280,1),  round(pression_bmp280,1))
    # pause
    time.sleep(2)
    
except KeyboardInterrupt :
    GPIO.cleanup()
    print ("Au revoir...")

