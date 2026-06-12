import pandas as pd

# Load datasets
disease = pd.read_csv("data/raw/disease_cases.csv")
weather = pd.read_csv("data/raw/weather_data.csv")

# Merge on district + date
df = pd.merge(disease, weather, on=["district", "date"])

# Sort data
df = df.sort_values(["district", "date"])

# Create lag features (previous week cases)
df["dengue_prev_week"] = df.groupby("district")["dengue_cases"].shift(1)
df["malaria_prev_week"] = df.groupby("district")["malaria_cases"].shift(1)

# Fill missing values from lag
df.fillna(0, inplace=True)

# Seasonal feature
df["month"] = pd.to_datetime(df["date"]).dt.month

# High-risk flag
df["high_risk"] = (
    (df["dengue_cases"] > 20) |
    (df["malaria_cases"] > 15)
).astype(int)

# Save processed dataset
df.to_csv("data/processed/final_dataset.csv", index=False)

print("Feature engineering complete!")
print("Final dataset shape:", df.shape)
print(df.head())