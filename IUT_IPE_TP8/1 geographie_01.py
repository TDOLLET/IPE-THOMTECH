# importation des librairies utiles
import requests
import pprint

# Demander à l'utilisateur un pays
pays = str(input("Pour quel pays souhaitez-vous des informations ? "))


# Récupération des infos via restcountries.eu
url = "https://restcountries.com/v3.1/name/"+pays
reponse = requests.request("GET", url)

# Décodage des données du pays au format JSON
donnees_json = reponse.json()
# Affichage brut mais structuré des données
pprint.pprint(donnees_json)

Region=donnees_json[0]['region']
Population=donnees_json[0]['population']
Capital=donnees_json[0]['capital'][0]


print("\n\nPAYS",pays.upper(),"\n\nRegion :", Region,"\nPopulation :",Population,"\nCapital :",Capital)
