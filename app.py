import streamlit as st
import pickle
import pandas as pd
import time

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Salary Pulse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# LOAD MODEL
# =========================================================
@st.cache_resource
def load_model():
    try:
        with open("dt_model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_model()

# =========================================================
# PREMIUM STYLES
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800;900&family=Inter:wght@300;400;600&display=swap');

.stApp {
    background:
        radial-gradient(circle at top, rgba(79,70,229,0.25), rgba(2,6,23,0.92)),
        url("https://png.pngtree.com/thumb_back/fh260/background/20240801/pngtree-vintage-one-dollar-bill-and-gold-coins-macro-background-image_16124152.jpg");
    background-size: cover;
    background-position: center;
}

/* HEADER */
.hero-box {
    text-align: center;
    padding: 48px;
    margin-bottom: 40px;
    border-radius: 26px;
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    backdrop-filter: blur(18px);
    box-shadow: 0 30px 80px rgba(0,0,0,0.55);
}

.hero-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 60px;
    font-weight: 900;
    background: linear-gradient(90deg, #22D3EE, #00E5FF, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 18px;
    color: #e0e7ff;
    margin-top: 12px;
}

/* INPUTS */
div[data-baseweb="select"] > div, input {
    background: rgba(255,255,255,0.10) !important;
    border-radius: 14px !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
}

label {
    font-size: 12px !important;
    color: #c7d2fe !important;
    text-transform: uppercase;
}

/* BUTTON */
.stButton > button {
    width: 360px;
    display: block;
    margin: auto;
    background: linear-gradient(135deg, #00E5FF, #4F46E5);
    color: #020617;
    font-size: 20px;
    font-weight: 900;
    padding: 16px;
    border-radius: 18px;
    border: none;
    box-shadow: 0 25px 60px rgba(79,70,229,0.6);
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-4px) scale(1.04);
    box-shadow: 0 35px 90px rgba(0,229,255,0.75);
}

/* RESULT */
.result-box {
    max-width: 780px;
    margin: 60px auto;
    text-align: center;
    padding: 50px;
    border-radius: 28px;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(20px);
    border-top: 4px solid #00E5FF;
    box-shadow: 0 40px 100px rgba(0,0,0,0.7);
}

.salary-text {
    font-family: 'Montserrat', sans-serif;
    font-size: 78px;
    font-weight: 900;
    background: linear-gradient(90deg, #22D3EE, #00E5FF, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="hero-box">
    <div class="hero-title">AI Salary Pulse</div>
    <div class="hero-sub">Premium Compensation Forecasting for Global AI Careers</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# INPUTS
# =========================================================
col1, col2 = st.columns(2)

with col1:
    job_tit = st.selectbox("Job Title", [
        'AI Research Scientist','AI Software Engineer','AI Specialist',
        'NLP Engineer','AI Consultant','AI Architect',
        'Principal Data Scientist','Data Analyst',
        'Machine Learning Engineer','Data Engineer'
    ])
    exp_lvl = st.selectbox("Experience Level", ['EN','MI','SE','EX'])
    emp_type = st.selectbox("Employment Type", ['FT','CT','PT','FL'])
    year_exp = st.selectbox("Years of Experience", list(range(0, 21)))
    industry = st.selectbox("Industry Domain", ['Technology','Finance','Healthcare','Education','Consulting'])
    remote_ratio = st.selectbox("Remote Ratio (%)", [0, 50, 100])

with col2:
    cmp_loc = st.selectbox("Company Location", ['India','United States','United Kingdom','Germany','Canada'])
    cmp_size = st.selectbox("Company Size", ['S','M','L'])
    emp_residency = st.selectbox("Employee Residence", ['India','United States','United Kingdom','Germany','Canada'])
    edu_required = st.selectbox("Education Level", ['Bachelor','Master','PhD'])
    job_descrp_len = st.number_input("Job Description Length", 50, 5000, 1500, step=50)
    benfit_score = st.number_input("Benefits Score", 0.0, 10.0, 7.5, step=0.1)

st.markdown("<br><br>", unsafe_allow_html=True)

# =========================================================
# BUTTON
# =========================================================
left, center, right = st.columns([4,4,4])
with center:
    predict_btn = st.button("Calculate Salary")

# scroll anchor
st.markdown("<div id='salary-output'></div>", unsafe_allow_html=True)

# =========================================================
# OUTPUT
# =========================================================
if predict_btn and model:

    st.markdown("""
    <script>
    document.getElementById("salary-output").scrollIntoView({behavior: "smooth"});
    </script>
    """, unsafe_allow_html=True)

    input_df = pd.DataFrame([{
        "job_title": job_tit,
        "experience_level": exp_lvl,
        "employment_type": emp_type,
        "company_location": cmp_loc,
        "company_size": cmp_size,
        "employee_residence": emp_residency,
        "remote_ratio": remote_ratio,
        "education_required": edu_required,
        "years_experience": year_exp,
        "industry": industry,
        "job_description_length": job_descrp_len,
        "benefits_score": benfit_score
    }])

    final_salary = model.predict(input_df)[0]

    container = st.empty()
    steps = 40
    value = 0
    step = final_salary / steps

    for _ in range(steps):
        value += step
        container.markdown(f"""
        <div class="result-box">
            <h3>Estimated Compensation</h3>
            <div class="salary-text">${int(value):,}</div>
            <p style="opacity:0.75;">Processing global salary intelligence…</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.06)

    container.markdown(f"""
    <div class="result-box">
        <h3>Estimated Compensation</h3>
        <div class="salary-text">${int(final_salary):,}</div>
        <p style="color:#00E5FF;">✔ Prediction Complete</p>
    </div>
    """, unsafe_allow_html=True)

elif predict_btn and not model:
    st.error("⚠️ Model file 'dt_model.pkl' not found.")
