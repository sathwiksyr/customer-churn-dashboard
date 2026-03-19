import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(page_title="Churn Analytics System", layout="wide")

# ---------------- STYLE (PREMIUM UI) ---------------- #
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00C9A7;
}

.stButton>button {
    background: linear-gradient(90deg, #FF4B4B, #FF6F61);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-weight: bold;
}

.stMetric {
    background-color: #1E1E2F;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN SYSTEM ---------------- #
def login():
    st.title("🔐 Login to Churn Analytics System")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["login"] = True
        else:
            st.error("❌ Invalid Username or Password")

# ---------------- LOAD MODEL ---------------- #
@st.cache_resource
def load_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    model_path = os.path.join(BASE_DIR, "model", "churn_model.pkl")
    encoder_path = os.path.join(BASE_DIR, "model", "encoders.pkl")

    model = pickle.load(open(model_path, 'rb'))
    encoders = pickle.load(open(encoder_path, 'rb'))

    return model, encoders

# ---------------- MAIN APP ---------------- #
def main_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(BASE_DIR, "data", "churn.csv")

    model, encoders = load_model()
    df = pd.read_csv(data_path)

    # ---------------- SIDEBAR ---------------- #
    st.sidebar.title("📊 Navigation")
    menu = st.sidebar.radio("Go to", ["Home", "Predict", "Analytics", "About"])

    # ---------------- HOME ---------------- #
    if menu == "Home":
        st.title("📊 Customer Churn Prediction System")

        st.markdown("""
        ### 🚀 Project Overview
        - Machine Learning based churn prediction  
        - Interactive analytics dashboard  
        - Real-world telecom dataset  

        ### 🎯 Key Features
        ✔ Predict churn probability  
        ✔ Data insights visualization  
        ✔ Business decision support  
        """)

    # ---------------- PREDICT ---------------- #
    elif menu == "Predict":
        st.title("🔍 Predict Customer Churn")

        col1, col2 = st.columns(2)

        with col1:
            tenure = st.slider("Tenure (Months)", 0, 72)
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])

        with col2:
            monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0)
            internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

        # Encoding
        contract_enc = encoders["Contract"].transform([contract])[0]
        internet_enc = encoders["InternetService"].transform([internet])[0]

        # Base input
        input_data = pd.DataFrame({
            "tenure": [tenure],
            "MonthlyCharges": [monthly_charges],
            "Contract": [contract_enc],
            "InternetService": [internet_enc]
        })

        # ✅ Fix feature mismatch
        input_data = input_data.reindex(columns=model.feature_names_in_, fill_value=0)

        if st.button("Predict"):
            prob = model.predict_proba(input_data)[0][1]
            result = model.predict(input_data)[0]

            st.subheader("📊 Prediction Result")

            # Metric
            st.metric("Churn Probability", f"{prob*100:.2f}%")

            # Progress bar
            st.progress(int(prob * 100))

            # Result
            if result == 1:
                st.error("⚠️ High Risk: Customer likely to churn")
            else:
                st.success("✅ Low Risk: Customer will stay")

            # Insight
            if prob > 0.7:
                st.warning("⚡ High risk — take action immediately!")
            elif prob > 0.4:
                st.info("⚠️ Medium risk — monitor customer.")
            else:
                st.success("👍 Low risk — stable customer.")

    # ---------------- ANALYTICS ---------------- #
    elif menu == "Analytics":
        st.title("📊 Data Insights")

        col3, col4 = st.columns(2)

        with col3:
            fig, ax = plt.subplots()
            sns.countplot(x="Contract", hue="Churn", data=df, ax=ax)
            st.pyplot(fig)

        with col4:
            fig2, ax2 = plt.subplots()
            sns.histplot(data=df, x="tenure", hue="Churn", bins=20)
            st.pyplot(fig2)

        st.subheader("📂 Sample Data")
        st.dataframe(df.sample(5))

    # ---------------- ABOUT ---------------- #
    elif menu == "About":
        st.title("👨‍💻 About Project")

        st.markdown("""
        **Customer Churn Prediction & Analytics System**

        Built using:
        - Machine Learning (Python)
        - Streamlit Web App
        - Power BI Dashboard

        **Key Insights:**
        - Early customers churn more  
        - High charges increase churn  
        - Contract type impacts retention  

        **Author:**  
        Sathwik S.Y.R  
        """)

        st.markdown("🔗 [GitHub Repo](https://github.com/sathwiksyr/customer-churn-dashboard)")

# ---------------- FLOW ---------------- #
if "login" not in st.session_state:
    st.session_state["login"] = False

if st.session_state["login"]:
    main_app()
else:
    login()