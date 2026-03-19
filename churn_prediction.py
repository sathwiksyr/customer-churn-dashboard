# 🚀 Customer Churn Prediction - Final Clean Code

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("data/churn.csv")

# Drop unnecessary column
if "customerID" in df.columns:
    df.drop("customerID", axis=1, inplace=True)

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')

# Fill missing values
df["TotalCharges"].fillna(df["TotalCharges"].median(), inplace=True)

# -------------------------------
# Encode categorical variables
# -------------------------------
encoders = {}

for col in df.columns:
    if df[col].dtype == 'object':
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

# Save encoders (IMPORTANT for app)
pickle.dump(encoders, open("model/encoders.pkl", "wb"))

# -------------------------------
# Split data
# -------------------------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train Models
# -------------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(),
    "Random Forest": RandomForestClassifier()
}

results = {}

best_model = None
best_acc = 0

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    results[name] = acc

    print(f"\n{name} Accuracy: {acc:.4f}")
    print(classification_report(y_test, y_pred))

    if acc > best_acc:
        best_acc = acc
        best_model = model

# Save best model
pickle.dump(best_model, open("model/churn_model.pkl", "wb"))

print(f"\n✅ Best Model Saved with Accuracy: {best_acc:.4f}")

# -------------------------------
# Model Comparison Plot
# -------------------------------
plt.figure(figsize=(6,4))
plt.bar(results.keys(), results.values())
plt.title("Model Accuracy Comparison")
plt.xlabel("Models")
plt.ylabel("Accuracy")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("images/model_accuracy.png")
plt.show()

# -------------------------------
# Feature Importance (Random Forest)
# -------------------------------
rf_model = models["Random Forest"]

rf_model.fit(X_train, y_train)

importance = rf_model.feature_importances_
features = X.columns

feat_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

print("\nTop Important Features:\n", feat_df.head())

# Plot feature importance
plt.figure(figsize=(6,4))
sns.barplot(x="Importance", y="Feature", data=feat_df.head(10))
plt.title("Top 10 Important Features Affecting Churn")
plt.tight_layout()
plt.savefig("images/feature_importance.png")
plt.show()

# -------------------------------
# Business Insights
# -------------------------------
print("\n📊 Business Insights:")
print("- Customers with higher monthly charges are more likely to churn.")
print("- Customers with shorter tenure show higher churn rates.")
print("- Contract type plays a major role in churn behavior.")