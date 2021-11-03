#TP4 EX3
#HTML - AFFICHER MESSAGE SUR LA MATRICE
from flask import Flask
from flask import render_template
from flask import request, url_for
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()
bleu = (4,41,99)
orange = (252,177,37)

serveur_web = Flask(__name__)

#definir le texte à afficher selon le chemn de l'URL
@serveur_web.route('/')    #page racine
def principal ():
    return render_template('Ex03.html')
         
@serveur_web.route('/change/',methods = ['POST'])
def change():
    if request.method == 'POST' :
        message_a_afficher = request.form['message']
        if request.form['switch'] == 'Envoyer' :    
            sense.set_rotation(180)
            sense.show_message(message_a_afficher,text_colour=[255,255,0],back_colour=[0,0,255])
            time.sleep(0.3)
            sense.clear()
    return render_template('Ex03.html')
            

#programme principal
serveur_web.debug = False
serveur_web.run(host="0.0.0.0")
