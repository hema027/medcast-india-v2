import streamlit as st
import requests
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="🦠 MedCast India",
    page_icon="🦠",
    layout="wide"
)

# ---------------------------
# SESSION STATE
# ---------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.title("🦠 MedCast India")

    st.info("""
    AI-powered Disease Outbreak Prediction Platform

    Technologies:
    • FastAPI
    • XGBoost
    • Streamlit
    • Machine Learning
    • Public Health Analytics
    """)

    st.markdown("---")

    st.subheader("🔗 API Endpoint")

    st.code(
"""
POST /predict

Returns:
{
    "risk_probability": 0.82,
    "high_risk_prediction": 1
}
"""
    )

    st.markdown("---")

    st.subheader("🏗 Architecture")

    st.code(
"""
User
 ↓
Streamlit Dashboard
 ↓
FastAPI Backend
 ↓
XGBoost Model
 ↓
Disease Risk Prediction
"""
    )

# ---------------------------
# MAIN TITLE
# ---------------------------
st.title("🦠 MedCast India")
st.subheader("AI-Powered Disease Outbreak Predictor")

st.write(
    "Predict outbreak risk using health, climate and historical disease data."
)

st.divider()

# ---------------------------
# INPUTS
# ---------------------------
st.header("📊 Enter Health & Weather Data")

col1, col2 = st.columns(2)

with col1:
    population_density = st.number_input(
        "Population Density",
        min_value=100,
        max_value=5000,
        value=800
    )

    dengue_cases = st.number_input(
        "Dengue Cases",
        min_value=0,
        max_value=1000,
        value=20
    )

    malaria_cases = st.number_input(
        "Malaria Cases",
        min_value=0,
        max_value=1000,
        value=10
    )

    typhoid_cases = st.number_input(
        "Typhoid Cases",
        min_value=0,
        max_value=1000,
        value=8
    )

    rainfall_mm = st.number_input(
        "Rainfall (mm)",
        min_value=0,
        max_value=500,
        value=120
    )

with col2:
    temperature_c = st.number_input(
        "Temperature (°C)",
        min_value=0,
        max_value=60,
        value=30
    )

    humidity_percent = st.number_input(
        "Humidity (%)",
        min_value=0,
        max_value=100,
        value=70
    )

    dengue_prev_week = st.number_input(
        "Dengue Prev Week",
        min_value=0,
        max_value=1000,
        value=15
    )

    malaria_prev_week = st.number_input(
        "Malaria Prev Week",
        min_value=0,
        max_value=1000,
        value=9
    )

    month = st.slider(
        "Month",
        min_value=1,
        max_value=12,
        value=7
    )

st.divider()

# ---------------------------
# PREDICT BUTTON
# ---------------------------
if st.button("🔍 Predict Risk", use_container_width=True):

    payload = {
        "population_density": population_density,
        "dengue_cases": dengue_cases,
        "malaria_cases": malaria_cases,
        "typhoid_cases": typhoid_cases,
        "rainfall_mm": rainfall_mm,
        "temperature_c": temperature_c,
        "humidity_percent": humidity_percent,
        "dengue_prev_week": dengue_prev_week,
        "malaria_prev_week": malaria_prev_week,
        "month": month
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=payload,
            timeout=10
        )

        if response.status_code != 200:
            st.error(f"Backend Error: {response.text}")
            st.stop()

        result = response.json()

    except requests.exceptions.RequestException:
        st.error("🚨 FastAPI backend is not running.")
        st.code("uvicorn app.main:app --reload")
        st.stop()

    probability = float(result["risk_probability"])

    # ---------------------------
    # RESULT SECTION
    # ---------------------------
    st.header("🧠 Risk Analysis")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Risk Probability",
            f"{probability:.2%}"
        )

    with c2:
        st.metric(
            "Prediction",
            "High Risk"
            if result["high_risk_prediction"] == 1
            else "Low Risk"
        )

    st.progress(min(probability, 1.0))

    # ---------------------------
    # RISK LEVELS
    # ---------------------------
    if probability >= 0.7:

        st.error("🔴 HIGH RISK ZONE")

        st.subheader("🚨 Recommended Actions")

        st.markdown("""
        - Increase mosquito control measures
        - Deploy medical teams
        - Issue public health alerts
        - Monitor hospitals closely
        - Increase testing and surveillance
        - Activate emergency response units
        """)

    elif probability >= 0.4:

        st.warning("🟠 MODERATE RISK ZONE")

        st.subheader("⚠ Recommended Actions")

        st.markdown("""
        - Monitor disease trends
        - Increase awareness campaigns
        - Prepare healthcare facilities
        - Track weekly disease growth
        """)

    else:

        st.success("🟢 LOW RISK ZONE")

        st.subheader("✅ Recommended Actions")

        st.markdown("""
        - Continue routine monitoring
        - Maintain sanitation programs
        - Encourage preventive healthcare
        - Monitor environmental conditions
        """)

    # ---------------------------
    # DISEASE CHART
    # ---------------------------
    st.divider()

    st.subheader("📊 Disease Distribution")

    chart_data = pd.DataFrame({
        "Disease": [
            "Dengue",
            "Malaria",
            "Typhoid"
        ],
        "Cases": [
            dengue_cases,
            malaria_cases,
            typhoid_cases
        ]
    })

    st.bar_chart(
        chart_data.set_index("Disease")
    )

    # ---------------------------
    # SAVE HISTORY
    # ---------------------------
    st.session_state.history.append({
        "Month": month,
        "Risk Probability": round(probability, 4),
        "Prediction":
        "High Risk"
        if result["high_risk_prediction"] == 1
        else "Low Risk"
    })

    # ---------------------------
    # RAW OUTPUT
    # ---------------------------
    st.divider()

    st.subheader("📋 Raw Model Output")

    st.json(result)

# ---------------------------
# HISTORY
# ---------------------------
if st.session_state.history:

    st.divider()

    st.subheader("📈 Prediction History")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

    csv = history_df.to_csv(index=False)

    st.download_button(
        "⬇ Download History CSV",
        csv,
        file_name="prediction_history.csv",
        mime="text/csv"
    )