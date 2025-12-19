import streamlit as st
import pickle
import pandas as pd
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Salary Pulse",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    try:
        with open("dt_model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

model = load_model()

# ---------------- STYLES ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;900&family=Inter:wght@300;400;600&display=swap');
.stApp {
    background:
        linear-gradient(rgba(2,6,2,0.92), rgba(2,6,2,0.92)),
        url("https://png.pngtree.com/thumb_back/fh260/background/20240801/pngtree-vintage-one-dollar-bill-and-gold-coins-macro-background-image_16124152.jpg");
    background-size: cover;
    background-position: center;
}

/* HEADER */
.hero-box {
    text-align: center;
    padding: 40px;
    margin-bottom: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
}

.hero-title {
    font-family: 'Montserrat', sans-serif;
    font-size: 56px;
    font-weight: 900;
    background: linear-gradient(90deg, #00E5FF, #4F46E5);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    font-size: 18px;
    color: #c7d2fe;
    margin-top: 10px;
}

/* INPUTS */
div[data-baseweb="select"] > div, input {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: white !important;
}

label {
    font-size: 13px !important;
    color: #c7d2fe !important;
    text-transform: uppercase;
}

/* BUTTON */
.stButton > button {
    width: 320px;
    display: block;
    margin: auto;
    background: linear-gradient(135deg, #00E5FF, #4F46E5);
    color: #000;
    font-size: 20px;
    font-weight: 800;
    padding: 14px;
    border-radius: 14px;
    border: none;
    text-transform: uppercase;
}

/* RESULT */
.result-box {
    max-width: 720px;
    margin: 40px auto;
    text-align: center;
    padding: 40px;
    border-radius: 20px;
    background: rgba(255,255,255,0.08);
    border-top: 4px solid #00E5FF;
}

.salary-text {
    font-family: 'Montserrat', sans-serif;
    font-size: 72px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">AI Salary Pulse</div>
    <div class="hero-sub">Smart Compensation Forecasting for Global AI Careers</div>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
col1, col2 = st.columns(2)

with col1:
    job_tit = st.selectbox(
        "Job Title",
        [
            'AI Research Scientist','AI Software Engineer','AI Specialist',
            'NLP Engineer','AI Consultant','AI Architect',
            'Principal Data Scientist','Data Analyst',
            'Machine Learning Engineer','Data Engineer'
        ],
        help="Select the AI/ML role you are targeting."
    )

    exp_lvl = st.selectbox(
        "Experience Level",
        ['EN','MI','SE','EX'],
        help="EN: Entry | MI: Mid | SE: Senior | EX: Executive"
    )

    emp_type = st.selectbox(
        "Employment Type",
        ['FT','CT','PT','FL'],
        help="FT: Full-time | CT: Contract | PT: Part-time | FL: Freelance"
    )

    year_exp = st.selectbox(
        "Years of Experience",
        list(range(0, 21)),
        help="Total professional experience in relevant roles."
    )

    industry = st.selectbox(
        "Industry Domain",
        ['Technology','Finance','Healthcare','Education','Consulting'],
        help="Business sector where the job belongs."
    )

    remote_ratio = st.selectbox(
        "Remote Ratio (%)",
        [0, 50, 100],
        help="0% Onsite | 50% Hybrid | 100% Fully Remote"
    )

with col2:
    cmp_loc = st.selectbox(
        "Company Location",
        ['India','United States','United Kingdom','Germany','Canada'],
        help="Country where the employer is based."
    )

    cmp_size = st.selectbox(
        "Company Size",
        ['S','M','L'],
        help="S: Small | M: Medium | L: Large organization"
    )

    emp_residency = st.selectbox(
        "Employee Residence",
        ['India','United States','United Kingdom','Germany','Canada'],
        help="Country where the employee currently lives."
    )

    edu_required = st.selectbox(
        "Education Level",
        ['Bachelor','Master','PhD'],
        help="Minimum educational qualification required."
    )

    job_descrp_len = st.number_input(
        "Job Description Length",
        50, 5000, 1500, step=50,
        help="Length of job description indicating role complexity."
    )

    benfit_score = st.number_input(
        "Benefits Score",
        0.0, 10.0, 7.5, step=0.1,
        help="Overall benefits rating including bonuses and perks."
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- BUTTON ----------------
left, center, right = st.columns([4,4,4])
with center:
    predict_btn = st.button("Calculate Salary")

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- OUTPUT ----------------
if predict_btn and model:

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

    result_container = st.empty()
    step = final_salary / 25
    current_val = 0

    for _ in range(25):
        current_val += step
        result_container.markdown(f"""
        <div class="result-box">
            <h3>Estimated Compensation</h3>
            <div class="salary-text">${int(current_val):,}</div>
            <p style="opacity:0.7;">Analyzing market trends...</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.02)

    result_container.markdown(f"""
    <div class="result-box">
        <h3>Estimated Compensation</h3>
        <div class="salary-text">${int(final_salary):,}</div>
        <p style="color:#00E5FF;">✔ Prediction Complete</p>
    </div>
    """, unsafe_allow_html=True)

elif predict_btn and not model:
    st.error("⚠️ Model file 'dt_model.pkl' not found.")
