# 📊 ChurnIQ — Customer Churn Prediction Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat&logo=streamlit)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?style=flat&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> A full end-to-end Machine Learning web app that predicts customer churn in real-time using the IBM Telco dataset.

🔗 **Live Demo:** [customer-churn-dashboard2006.streamlit.app](https://customer-churn-dashboard2006.streamlit.app/)

---

## 🚀 Features

- 🔐 **Login system** — secured with username & password
- 🔍 **Real-time prediction** — enter customer details and get instant churn probability
- 📊 **Analytics dashboard** — churn by contract type, payment method, tenure distribution
- 🎯 **Risk gauge** — visual indicator (Low / Medium / High risk)
- 🔎 **Key factors** — shows which inputs are driving the prediction
- ⬇️ **Export** — download data as CSV or PDF report
- ⚡ **Spinner animation** — smooth UX while model runs

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web dashboard framework |
| scikit-learn | Random Forest ML model |
| Pandas & NumPy | Data wrangling |
| Plotly | Interactive charts |
| ReportLab | PDF generation |
| IBM Telco Dataset | 7,043 customer records |

---

## 📁 Project Structure

```
Customer Churn Prediction project/
│
├── ChurnIQ/                  # Main Streamlit app
│   ├── app.py                # Entry point
│   ├── config.py             # Constants & Plotly theme
│   ├── loader.py             # Model & data loading
│   ├── requirements.txt      # Python dependencies
│   │
│   ├── assets/
│   │   └── style.css         # Custom CSS styles
│   │
│   └── components/
│       ├── __init__.py
│       ├── login.py          # Login page
│       ├── home.py           # Home tab
│       ├── predict.py        # Predict tab
│       ├── analytics.py      # Analytics tab
│       └── about.py          # About tab
│
├── model/
│   ├── churn_model.pkl       # Trained Random Forest model
│   └── encoders.pkl          # Label encoders
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

**3. Run the app**
```bash
streamlit run ChurnIQ/app.py
```

**4. Login credentials**
```
Username: admin
Password: 1234
```

---

## 🤖 Model Details

- **Algorithm:** Random Forest Classifier
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

## 👤 Developer

**Sathwik S.Y.R** — Big Data Engineering Student

Skills: `Python` `Machine Learning` `Power BI` `SQL` `Streamlit` `Apache Spark`

---

## 📄 License

This project is licensed under the MIT License.
