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

population_density = {
    district: np.random.randint(200, 1200)
    for district in districts
}

start_date = datetime(2023, 1, 1)
weeks = 156  # 3 years

rows = []

for district in districts:

    density = population_density[district]

    for week in range(weeks):

        date = start_date + timedelta(weeks=week)

        month = date.month

        monsoon_factor = 1

        if month in [6, 7, 8, 9]:
            monsoon_factor = 3

        dengue = max(
            0,
            int(
                np.random.normal(
                    15 * monsoon_factor + density / 150,
                    5
                )
            )
        )

        malaria = max(
            0,
            int(
                np.random.normal(
                    10 * monsoon_factor + density / 200,
                    4
                )
            )
        )

        typhoid = max(
            0,
            int(
                np.random.normal(
                    8 + density / 300,
                    3
                )
            )
        )

        rows.append([
            district,
            date.date(),
            density,
            dengue,
            malaria,
            typhoid
        ])

df = pd.DataFrame(
    rows,
    columns=[
        "district",
        "date",
        "population_density",
        "dengue_cases",
        "malaria_cases",
        "typhoid_cases"
    ]
)

df.to_csv("data/raw/disease_cases.csv", index=False)

print("Dataset created successfully!")
print(df.head())
print(f"Total rows: {len(df)}")