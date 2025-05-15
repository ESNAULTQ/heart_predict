import streamlit as st
import requests

# Titre principal
st.title("🫀 Prédiction du Risque de Maladie Cardiaque")
st.subheader("Entrez les données cliniques du patient pour obtenir une estimation automatique.")

# 📍 URL de l'API FastAPI
API_URL = "http://localhost:8000/predict"

# 🧾 Champs de saisie
with st.form("formulaire"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Âge", min_value=18, max_value=100, value=60)
        sex = st.selectbox("Sexe", ["M", "F"])
        chest_pain = st.selectbox("Type de douleur thoracique", ["ATA", "NAP", "ASY", "TA"])
        resting_bp = st.number_input("Pression artérielle au repos (mm Hg)", value=120)
        cholesterol = st.number_input("Cholestérol (mg/dl)", value=200)
        fasting_bs = st.selectbox("Glycémie à jeun > 120 mg/dl ?", [0, 1])

    with col2:
        ecg = st.selectbox("Résultat ECG au repos", ["Normal", "ST", "LVH"])
        max_hr = st.number_input("Fréquence cardiaque max", value=150)
        angina = st.selectbox("Angine à l’effort", ["Y", "N"])
        oldpeak = st.number_input("Oldpeak (dépression ST)", value=1.0, step=0.1, format="%.1f")
        st_slope = st.selectbox("Pente ST", ["Up", "Flat", "Down"])

    # Bouton de validation
    submitted = st.form_submit_button("💡 Prédire")

# 🔄 Envoi de la requête
if submitted:
    payload = {
        "Age": age,
        "Sex": sex,
        "ChestPainType": chest_pain,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": fasting_bs,
        "RestingECG": ecg,
        "MaxHR": max_hr,
        "ExerciseAngina": angina,
        "Oldpeak": oldpeak,
        "ST_Slope": st_slope
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ Prédiction : {'Présence de maladie cardiaque' if result['prediction'] == 1 else 'Absence de maladie cardiaque'}")
            st.metric("Probabilité (HeartDisease = 1)", f"{result['probability_1']*100:.1f}%")
        else:
            st.error(f"Erreur API : code {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Impossible de se connecter à l'API. Assurez-vous qu'elle est bien lancée.")
