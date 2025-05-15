from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Charger le pipeline (OneHotEncoder + LogisticRegression)
model = joblib.load("logistic_pipeline.pkl")

# Créer l'app
app = FastAPI()

# Définir le modèle de données attendu
class PatientData(BaseModel):
    Age: int
    Sex: str
    ChestPainType: str
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    RestingECG: str
    MaxHR: int
    ExerciseAngina: str
    Oldpeak: float
    ST_Slope: str

@app.post("/predict")
def predict(data: PatientData):
    # 🔁 Convertir en DataFrame avec noms de colonnes
    input_dict = data.dict()
    input_df = pd.DataFrame([input_dict])  # ✅ important : garde les noms des colonnes

    # Prédiction
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]  # proba que HeartDisease = 1

    return {
        "prediction": int(prediction),
        "probability_1": round(float(probability), 4)
    }
