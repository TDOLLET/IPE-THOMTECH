#serveur web
#TP4 Exo 2
#HTML
#Contrôle a distance de la lumière
from sense_hat import SenseHat
import random
import time
from flask import Flask
from flask import render_template
from flask import request, url_for
import socket

sense=SenseHat()

b = (255,255,255)
n = (0,0,0)

lampe = [n,n,b,b,b,b,n,n,
         n,b,b,b,b,b,b,n,
         b,b,b,b,b,b,b,b,
         b,b,b,b,b,b,b,b,
         b,b,b,b,b,b,b,b,
         b,b,b,b,b,b,b,b,
         n,b,b,b,b,b,b,n,
         n,n,b,b,b,b,n,n]


serveur_web = Flask(__name__)

#definir le texte à afficher selon le chemn de l'URL
@serveur_web.route('/')    #page racine
def principal ():
    return render_template('Ex02.html')
         
@serveur_web.route('/change/',methods = ['POST'])
def change():
    if request.method == 'POST' :
        if request.form['switch'] == 'Allumer':
            sense.set_pixels(lampe)
        elif request.form['switch'] == 'Eteindre' :
            sense.clear()
    return render_template('Ex02.html')
            

#programme principal
serveur_web.debug = False
serveur_web.run(host="0.0.0.0")
