# 📊 ChurnIQ × 🔭 DataLens — Intelligence Platform
 
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat&logo=scikit-learn)
![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-purple?style=flat)
![XGBoost](https://img.shields.io/badge/XGBoost-Gradient_Boost-green?style=flat)
 
> A full end-to-end Intelligence Platform combining **ChurnIQ** (Customer Churn Prediction with Explainable AI) and **DataLens** (Universal Analytics Studio for any CSV dataset).
 
🔗 **Live Demo:** [customer-churn-dashboard2006.streamlit.app](https://customer-churn-dashboard2006.streamlit.app/)
 
---
 
## 🧠 Platform Overview
 
| Tool | Description |
|------|-------------|
| 📊 **ChurnIQ** | Churn Intelligence — ML-powered customer churn prediction |
| 🔭 **DataLens** | Universal Analytics Studio — auto-dashboard for any CSV |
 
After login, users choose which tool to open. Both tools are accessible from a clean landing page with a **Switch tool** button to move between them.
 
---
 
## 🚀 Features
 
### 📊 ChurnIQ — Churn Intelligence
- 🔐 **Secure signup & login** — user accounts with SHA-256 hashed passwords
- 🔍 **Real-time prediction** — enter customer details and get instant churn probability
- 🧠 **Explainable AI (SHAP)** — visual bar chart showing why a customer is predicted to churn
- 💡 **Smart recommendations** — actionable business strategies (High / Medium / Low impact)
- 🤖 **Model comparison** — Random Forest vs Logistic Regression vs SVM vs XGBoost
- 📋 **Accuracy metrics** — Accuracy, Precision, Recall, F1 Score, ROC AUC for all models
- 📊 **Analytics dashboard** — churn by contract type, payment method, tenure distribution
- 🎯 **Risk gauge** — visual indicator (Low / Medium / High risk)
- ⬇️ **Export** — download data as CSV or full PDF report with model metrics
- ⚡ **Spinner animation** — smooth UX while model runs
 
### 🔭 DataLens — Universal Analytics Studio
- 📂 **Upload any CSV** — HR attrition, sales, finance, churn or any tabular data
- 🔍 **Smart column detection** — auto-detects target, tenure, charges, segment columns
- 📊 **Auto-built dashboard** — pie, bar, histogram, box charts generated instantly
- 🔧 **Override mapping** — manually correct any auto-detected column
- 📈 **All categorical breakdowns** — auto-charts for every categorical column
- 🔄 **Refresh button** — reload data instantly
- ⬇️ **Export** — download processed CSV
 
---
 
## 🛠 Tech Stack
 
| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web dashboard framework |
| scikit-learn | Random Forest, Logistic Regression, SVM |
| XGBoost | Gradient boosting classifier |
| SHAP | Explainable AI & feature importance |
| Pandas & NumPy | Data wrangling |
| Plotly | Interactive charts |
| ReportLab | PDF report generation |
| IBM Telco Dataset | 7,043 customer records |
 
---
 
## 📁 Project Structure
 
```
Customer Churn Prediction project/
│
├── model.py                  # Train & compare all models (run once)
│
├── ChurnIQ/                  # Main Streamlit app
│   ├── app.py                # Entry point + landing page
│   ├── Config.py             # Constants & Plotly theme
│   ├── loader.py             # Model & data loading
│   ├── utils.py              # SHAP, recommendations, PDF, model comparison
│   ├── requirements.txt      # Python dependencies
│   │
│   ├── assets/
│   │   └── style.css         # Custom CSS styles
│   │
│   └── components/
│       ├── __init__.py
│       ├── auth.py           # Signup & login
│       ├── home.py           # Home tab
│       ├── predict.py        # Predict tab (SHAP + recommendations)
│       ├── analytics.py      # Analytics + model comparison
│       ├── about.py          # About tab
│       └── smart_upload.py   # DataLens — universal CSV analytics
│
├── model/
│   ├── churn_model.pkl       # Best trained model
│   ├── encoders.pkl          # Label encoders
│   ├── metrics.pkl           # All model metrics
│   ├── best_name.pkl         # Best model name
│   └── feature_names.pkl     # Feature names list
│
└── data/
    └── Churn.csv             # IBM Telco dataset
```
 
---
 
## ⚙️ Installation & Run Locally
 
**1. Clone the repo**
```bash
git clone https://github.com/sathwiksyr/customer-churn-dashboard.git
cd "Customer Churn Prediction project"
```
 
**2. Install dependencies**
```bash
pip install -r ChurnIQ/requirements.txt
```
 
**3. Train all models (run once)**
```bash
python model.py
```
This trains Random Forest, Logistic Regression, SVM and XGBoost, auto-selects the best model and saves all metrics.
 
**4. Run the app**
```bash
streamlit run ChurnIQ/app.py
```
 
**5. Sign up with any email** or use existing credentials.
 
---
 
## 🤖 Model Details
 
- **Algorithms compared:** Random Forest · Logistic Regression · SVM · XGBoost
- **Best model:** Auto-selected based on F1 Score
- **Dataset:** IBM Telco Customer Churn (7,043 records)
- **Features used:**
  - Tenure, Monthly Charges, Total Charges
  - Contract type, Internet service, Payment method
  - Senior citizen, Partner, Dependents
  - Tech support, Online security, Streaming services
  - Paperless billing, Phone service
 
---
 
## 📊 Dataset
 
IBM Telco Customer Churn dataset from [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
 
- 7,043 customer records
- 21 features
- Binary target: `Churn` (Yes / No)
- Churn rate: ~26.5%
 
---
 
## 📝 Conclusions
 
### Key Findings from the Data
 
- **Contract type is the strongest churn predictor** — customers on month-to-month contracts churn at a much higher rate (~42%) compared to one-year (~11%) or two-year (~3%) contracts. Encouraging long-term contracts is the single most effective retention strategy.
 
- **Tenure matters significantly** — customers who have been with the company for less than 12 months are at the highest risk of churning. The longer a customer stays, the less likely they are to leave.
 
- **Fiber optic users churn more** — despite being a premium service, fiber optic internet customers show higher churn rates, suggesting pricing or service quality issues that need to be addressed.
 
- **Electronic check payment increases churn risk** — customers paying via electronic check churn more than those using automatic bank transfers or credit cards, possibly indicating less commitment or financial instability.
 
- **Lack of support services drives churn** — customers without tech support, online security, or online backup are significantly more likely to churn. Bundling these services can improve retention.
 
- **Senior citizens are at higher risk** — senior citizen customers show elevated churn rates and may need dedicated support programs or pricing plans.
 
### Business Recommendations
 
| Action | Impact |
|--------|--------|
| Offer discounts for 1-year or 2-year contracts | High |
| Target new customers (< 12 months) with loyalty rewards | High |
| Improve fiber optic service quality or reprice | Medium |
| Bundle tech support & security into base plans | Medium |
| Switch customers from electronic check to auto-pay | Low |
 
### Model Performance
 
- The best model (auto-selected by F1 Score) successfully identifies high-risk customers with 80%+ accuracy.
- Explainable AI (SHAP) allows customer service teams to understand exactly why a customer is flagged.
- Smart recommendations give businesses actionable strategies to retain at-risk customers proactively.
- DataLens extends the platform beyond churn — any team can upload their own dataset and get instant insights.
 
---
 
