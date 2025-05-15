import requests

# L'URL de ton API (modifie le port si différent)
url = "http://localhost:8000/predict"

# Données à envoyer (elles doivent exactement correspondre au modèle)
data = {
    "Age": 52,
    "Sex": "M",
    "ChestPainType": "ATA",
    "RestingBP": 130,
    "Cholesterol": 250,
    "FastingBS": 0,
    "RestingECG": "Normal",
    "MaxHR": 150,
    "ExerciseAngina": "N",
    "Oldpeak": 1.2,
    "ST_Slope": "Up"
}

# Envoi de la requête POST
response = requests.post(url, json=data)

# Affichage du résultat
print(response.status_code)
print(response.json())
