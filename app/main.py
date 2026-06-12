from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

# Load trained model
model = joblib.load("models/disease_risk_model.pkl")

features = [
    "population_density",
    "dengue_cases",
    "malaria_cases",
    "typhoid_cases",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent",
    "dengue_prev_week",
    "malaria_prev_week",
    "month"
]

@app.get("/")
def home():
    return {"message": "MedCast India ML API is running"}

@app.post("/predict")
def predict(data: dict):

    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df[features])[0]
    probability = model.predict_proba(input_df[features])[0][1]

    return {
        "high_risk_prediction": int(prediction),
        "risk_probability": float(probability)
    }