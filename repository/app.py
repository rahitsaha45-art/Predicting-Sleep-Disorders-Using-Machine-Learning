
import streamlit as st
import pandas as pd
import joblib
import base64
import sklearn
print(sklearn.__version__)

# ==================================
# PAGE CONFIGURATION
# ==================================

st.set_page_config(
    page_title="Sleep Disorder Prediction",
    page_icon="😴",
    layout="wide"
)

# ==================================
# BACKGROUND DESIGN
# ==================================

def set_background(image_file):
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.65);
                z-index: -1;
            }}
            h1,h2,h3,h4,h5,h6 {{
                color: orange !important;
                font-weight: 900;
            }}
            .stMarkdown,
            label,
            p,
            div {{
                color: white;
            }}
            .stButton>button {{
                background-color: orange;
                color: black;
                font-weight: bold;
                width: 100%;
                border-radius: 12px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except:
        pass

# Optional
set_background("sleep_background.png")

# ==================================
# LOAD MODEL
# ==================================

@st.cache_resource
def load_model():
    # Load the correct saved artifacts file
    artifacts = joblib.load("sleep_disorder_artifacts.pkl")
    return artifacts["model"]

model = load_model()

# ==================================
# HEADER
# ==================================

st.title("😴 Sleep Disorder Prediction System")

st.markdown("""
This application predicts whether a patient is likely to have:

✅ None

⚠️ Insomnia

🚨 Sleep Apnea

using demographic, lifestyle and health information.
""")

st.markdown("---")

# ==================================
# INPUT SECTION
# ==================================

st.sidebar.header("Patient Information")

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
age = st.sidebar.slider("Age", 18, 80, 35)

occupation = st.sidebar.selectbox(
    "Occupation",
    [
        "Accountant",
        "Doctor",
        "Engineer",
        "Lawyer",
        "Manager",
        "Nurse",
        "Salesperson",
        "Scientist",
        "Software Engineer",
        "Teacher"
    ]
)

sleep_duration = st.sidebar.slider("Sleep Duration (Hours)", 4.0, 10.0, 7.0)
quality_of_sleep = st.sidebar.slider("Quality of Sleep", 1, 10, 7)
physical_activity = st.sidebar.slider("Physical Activity Level", 20, 100, 50)
stress_level = st.sidebar.slider("Stress Level", 1, 10, 5)

bmi_category = st.sidebar.selectbox(
    "BMI Category",
    [
        "Normal",
        "Overweight",
        "Obese"
    ]
)

heart_rate = st.sidebar.slider("Heart Rate", 50, 120, 72)
daily_steps = st.sidebar.slider("Daily Steps", 1000, 20000, 7000)
systolic_bp = st.sidebar.slider("Systolic Blood Pressure", 90, 180, 120)
diastolic_bp = st.sidebar.slider("Diastolic Blood Pressure", 60, 120, 80)

# Calculate extra engineering features required by your preprocessor pipeline
sleep_efficiency = quality_of_sleep / sleep_duration
steps_per_activity = daily_steps / (physical_activity + 1)
pulse_pressure = systolic_bp - diastolic_bp
mean_arterial_pressure = diastolic_bp + (systolic_bp - diastolic_bp) / 3

# ==================================
# CREATE INPUT DATAFRAME
# ==================================

input_df = pd.DataFrame({
    "Gender": [gender],
    "Age": [age],
    "Occupation": [occupation],
    "Sleep Duration": [sleep_duration],
    "Quality of Sleep": [quality_of_sleep],
    "Physical Activity Level": [physical_activity],
    "Stress Level": [stress_level],
    "BMI Category": [bmi_category],
    "Heart Rate": [heart_rate],
    "Daily Steps": [daily_steps],
    "Systolic_BP": [systolic_bp],
    "Diastolic_BP": [diastolic_bp],
    "Sleep_Efficiency": [sleep_efficiency],
    "Steps_per_Activity": [steps_per_activity],
    "Pulse_Pressure": [pulse_pressure],
    "Mean_Arterial_Pressure": [mean_arterial_pressure]
})

# ==================================
# SHOW INPUTS
# ================================== 

st.subheader("Patient Information Summary")

st.dataframe(
    input_df,
    use_container_width=True
)

st.markdown("---")

# ==================================
# PREDICTION
# ==================================

if st.button("Predict Sleep Disorder"):
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    class_mapping = {
        0: "Insomnia",
        1: "None",
        2: "Sleep Apnea"
    }

    predicted_class = class_mapping[prediction]
    st.subheader("Prediction Result")

    if predicted_class == "None":
        st.success(f"✅ Prediction: {predicted_class}")
    elif predicted_class == "Insomnia":
        st.warning(f"⚠️ Prediction: {predicted_class}")
    else:
        st.error(f"🚨 Prediction: {predicted_class}")

    # ===========================
    # PROBABILITY CHART
    # ===========================

    probability_df = pd.DataFrame({
        "Class": [
            "Insomnia",
            "None",
            "Sleep Apnea"
        ],
        "Probability": probabilities
    })

    st.subheader("Prediction Probabilities")
    st.bar_chart(probability_df.set_index("Class"))

    # ===========================
    # RISK SUMMARY
    # ===========================

    st.subheader("Risk Summary")
    st.info(
        f"""
        Age: {age}
        Sleep Duration: {sleep_duration} hrs
        Sleep Quality: {quality_of_sleep}/10
        Stress Level: {stress_level}/10
        BMI Category: {bmi_category}
        Daily Steps: {daily_steps}
        """
    )

# ==================================
# FOOTER
# ==================================

st.markdown("---")

st.markdown("""
### About This Project

**Models Evaluated**
- Logistic Regression
- Decision Tree
- Random Forest
- XGBoost

**Best Model Deployed**
- Logistic Regression (Selected for simplicity & interpretability)

**Project**
Predicting Sleep Disorders using Machine Learning

Developed by **Rahit Saha**
""")
