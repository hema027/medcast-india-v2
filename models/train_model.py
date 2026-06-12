import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import joblib

# Load dataset
df = pd.read_csv("data/processed/final_dataset.csv")

# Features & target
target = "high_risk"

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

X = df[features]
y = df[target]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "models/disease_risk_model.pkl")

print("\nModel saved successfully at models/disease_risk_model.pkl")