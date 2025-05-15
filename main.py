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
    try:
        input_df = pd.DataFrame([data.dict()])
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]
        return {
            "prediction": int(prediction),
            "probability_1": round(float(probability), 4)
        }
    except Exception as e:
        return {"error": str(e)}
