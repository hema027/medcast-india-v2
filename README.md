# MedCast India — Multi-Disease Epidemic Surge Predictor 🦟📈

> Forecasting district-level outbreak risk for Dengue, Malaria, and Typhoid across India using weather data, machine learning, and explainable AI.

---

## 🩺 Problem Statement

India reports over a million cases combined of dengue, malaria, and typhoid every year, with sharp seasonal surges that strain district-level healthcare systems. Outbreaks are heavily driven by climate factors — rainfall, temperature, and humidity — that create favorable conditions for mosquito breeding and waterborne pathogen spread, typically **2-8 weeks before case counts spike**.

Most existing public health dashboards report cases *after* they happen. There is a gap for a **proactive, explainable, district-level early warning system** that:

- Predicts surge **risk** for the next 4 weeks, per district, per disease
- Uses **publicly available weather and population data** (no expensive sensors)
- Explains **why** a district is flagged (which factors are driving the risk), so health officers can act on the *cause*, not just the alarm
- Is lightweight enough to run on free-tier infrastructure, making it deployable for resource-constrained district health departments

**MedCast India** addresses this gap with a forecasting pipeline that combines tree-based models, sequence models, and explainability tooling into a single dashboard.

---

## 🎯 Project Goals

1. Build disease-specific surge classifiers (will cases exceed an outbreak threshold in the next 4 weeks?)
2. Build a time-series forecaster for actual case-count trajectories
3. Make every prediction **explainable** — surface the top drivers (rainfall lag, humidity, prior case trend, etc.)
4. Package everything into an interactive dashboard usable by non-technical health officers
5. Deploy a free, publicly accessible demo

---

## 🛠️ Tech Stack & Why

| Tool | Role | Why this tool |
|---|---|---|
| **Python (pandas, numpy)** | Data wrangling, feature engineering | Industry standard for tabular time-series prep; lag/rolling-window features are trivial to compute |
| **Open-Meteo API** | Historical weather data (rainfall, temp, humidity) | Free, no API key required, has long historical archives for any lat/long — ideal for covering 50+ Indian districts |
| **IDSP / data.gov.in** | Disease case-count data | Authoritative Indian government source for disease surveillance, grounding the project in real public health data |
| **scikit-learn (Logistic Regression)** | Baseline model | Establishes an interpretable performance floor before adding model complexity — good ML practice and a strong talking point in interviews |
| **XGBoost** | Disease-specific surge classifiers | Handles tabular, non-linear, mixed-scale features (case counts + weather + lags) extremely well; fast to train and tune; near industry-standard for structured-data competitions |
| **PyTorch (LSTM)** | 4-week case-count forecasting | Captures temporal dependencies (8-week lookback) that tree models can't directly model — shows comfort with deep learning sequence models |
| **SHAP** | Model explainability | Converts "black-box" XGBoost output into per-feature contribution values — critical for a *health* application where decision-makers need to trust and act on a "why," not just a score |
| **FastAPI** | Backend serving layer | Modern, async, auto-documented (Swagger UI) Python API framework — production-grade way to serve ML models |
| **Streamlit** | Interactive dashboard | Fastest way to build a data-app UI in pure Python — lets the focus stay on ML rather than frontend engineering |
| **Hugging Face Spaces** | Free deployment | Zero-cost hosting for Streamlit apps with GPU/CPU support, giving the project a live, shareable demo link |
| **Plotly** | Charts in dashboard | Interactive, hover-friendly charts for forecasts and SHAP visualizations |

---

## 🏗️ System Architecture

```
                    ┌─────────────────────┐
                    │   Data Sources       │
                    │  IDSP case data      │
                    │  Open-Meteo weather  │
                    └─────────┬────────────┘
                              │
                    ┌─────────▼────────────┐
                    │ Feature Engineering   │
                    │ lags, rolling means,  │
                    │ population density    │
                    └─────────┬────────────┘
                              │
              ┌───────────────┼────────────────┐
              ▼               ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │ Logistic Reg  │ │   XGBoost    │ │  LSTM (torch) │
      │  (baseline)   │ │ (per disease)│ │ (4-wk forecast)│
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                 │
             └────────┬───────┴────────┬────────┘
                       ▼                ▼
                ┌─────────────┐  ┌─────────────┐
                │   SHAP       │  │  FastAPI     │
                │ explainability│ │  /predict    │
                └─────────────┘  └──────┬──────┘
                                         ▼
                                ┌─────────────────┐
                                │ Streamlit Dashboard│
                                │ (Hugging Face)    │
                                └─────────────────┘
```

---

## ✨ Key Features

- **Multi-disease support**: separate models for dengue, malaria, and typhoid, since each has different climate sensitivities
- **District-level granularity**: covers 50+ Indian districts spanning multiple climate zones
- **4-week-ahead forecasting**: gives health departments enough lead time to mobilize resources
- **Explainable risk scores**: each prediction comes with a SHAP-based breakdown of contributing factors (e.g., "rainfall 3 weeks ago," "current humidity," "case trend")
- **Model comparison**: baseline logistic regression vs. XGBoost vs. LSTM, with reported metrics (accuracy/F1 for classifiers, RMSE for forecaster)
- **Interactive dashboard**: district + disease selectors, color-coded risk badges (low/medium/high), forecast trend charts, and SHAP driver charts

---

## 📁 Project Structure

```
medcast-india-v2/
├── data/
│   ├── raw/              # raw IDSP + weather data, synthetic data generator
│   └── processed/        # feature-engineered datasets
├── models/                # trained model artifacts (.pkl, .pt)
├── api/                   # FastAPI backend (/predict, /health)
├── dashboard/             # Streamlit app
├── notebooks/             # EDA and experimentation notebooks
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

```bash
# Clone the repo
git clone https://github.com/<your-username>/medcast-india-v2.git
cd medcast-india-v2

# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate / fetch data
python data/raw/generate_synthetic_data.py
python data/raw/fetch_weather.py

# Run feature engineering + train models
python models/train_models.py

# Start the API
uvicorn api.main:app --reload

# Launch the dashboard
streamlit run dashboard/app.py
```

---

## 📊 Results (fill in after training)

| Model | Disease | Metric | Score |
|---|---|---|---|
| Logistic Regression (baseline) | Dengue | F1 | _TBD_ |
| XGBoost | Dengue | F1 | _TBD_ |
| XGBoost | Malaria | F1 | _TBD_ |
| XGBoost | Typhoid | F1 | _TBD_ |
| LSTM | All (4-wk forecast) | RMSE | _TBD_ |

---

## 🌐 Live Demo

🔗 [MedCast India on Hugging Face Spaces](#) *(add link after deployment)*

---

## 🔮 Future Improvements

- Incorporate real-time satellite-derived vegetation/water-body indices (linked to mosquito breeding grounds)
- Add population mobility data for cross-district spread modeling
- SMS/WhatsApp alert integration for district health officers
- Expand coverage beyond 50 districts to all of India

---

## 👤 Author

Built as part of an applied ML project exploring epidemic forecasting in low-resource public health settings.

