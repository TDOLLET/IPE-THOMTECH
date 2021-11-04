# importation des librairies utiles
import requests
import pprint

# Récupération des infos de population en France par département
URL_population = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=population-francaise-par-departement-2018&q=&lang=fr&rows=101&facet=departement"
reponse = requests.request("GET", URL_population)

# Décodage des données du pays au format JSON
population_json = reponse.json()

# Affichage brut mais structuré des données
#pprint.pprint(population_json)

# Extraction de la population du département d'Ille-et-Vilaine
departement="Ille-et-Vilaine"


for i in range(len(population_json["records"])-1):
    if((population_json["records"][i]["fields"]["departement"]==departement)):
        nombre_habitant=population_json["records"][i]["fields"]["population"]

print("La population de "+departement+" s'élève à "+str(nombre_habitant))
            