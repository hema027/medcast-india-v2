import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

districts = [
    "Bhopal","Indore","Jabalpur","Gwalior","Ujjain",
    "Sagar","Rewa","Satna","Ratlam","Dewas",
    "Nagpur","Pune","Mumbai","Nashik","Aurangabad",
    "Chennai","Coimbatore","Madurai","Salem","Trichy",
    "Bengaluru","Mysuru","Hubli","Mangalore","Belagavi",
    "Hyderabad","Warangal","Nizamabad","Karimnagar","Khammam",
    "Delhi","Noida","Ghaziabad","Gurugram","Faridabad",
    "Lucknow","Kanpur","Agra","Varanasi","Prayagraj",
    "Jaipur","Jodhpur","Kota","Ajmer","Udaipur",
    "Kolkata","Howrah","Durgapur","Siliguri","Asansol"
]

start_date = datetime(2023, 1, 1)
weeks = 156

rows = []

for district in districts:
    for week in range(weeks):

        date = start_date + timedelta(weeks=week)
        month = date.month

        rainfall = np.random.normal(20, 5)
        temperature = np.random.normal(28, 2)
        humidity = np.random.normal(60, 5)

        if month in [6, 7, 8, 9]:
            rainfall += np.random.normal(180, 20)
            humidity += 20
            temperature -= 2

        rows.append([
            district,
            date.date(),
            round(rainfall, 2),
            round(temperature, 2),
            round(humidity, 2)
        ])

df = pd.DataFrame(rows, columns=[
    "district",
    "date",
    "rainfall_mm",
    "temperature_c",
    "humidity_percent"
])

df.to_csv("data/raw/weather_data.csv", index=False)

print("Weather dataset generated successfully!")
print("Rows:", len(df))
print(df.head())