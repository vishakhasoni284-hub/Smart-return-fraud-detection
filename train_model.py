import pandas as pd
import numpy as np
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


df = pd.read_csv("ml/returns_data.csv")  # your generated data
df.head()
# Features for ML models
feature_cols = [
    "account_age_days",
    "total_orders",
    "total_returns",
    "product_price",
    "days_after_delivery",
    "product_condition",         # encoded later
    "high_value_product",
    "pickup_location_changed",
    "repeated_return_reason",
    "product_category"
]

lb = LabelEncoder()
# Convert categorical columns to numeric
df_encoded = df.copy()
df_encoded["product_condition"] = lb.fit_transform(df_encoded["product_condition"])
df_encoded["product_category"] = lb.fit_transform(df_encoded['product_category'])

# Features and target
X = df_encoded[feature_cols]
y = df_encoded["is_fraud"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

sc = StandardScaler()
X_train_sc = sc.fit_transform(X_train)

# FRAUD LOGIC 

class RuleBasedFraud:
    """
    Rule-based engine that returns fraud_score, risk, decision, and explanation
    """
    def predict(self, data):
        score = 0
        reasons = []

        # Ratio of returns
        if data["total_returns"] / max(data["total_orders"], 1) > 0.5:
            score += 0.25
            reasons.append("High return ratio")

        # New account
        if data["account_age_days"] < 100:
            score += 0.15
            reasons.append("New account")

        # High value product
        if data["product_price"] > 3000 or data.get("high_value_product", False):
            score += 0.20
            reasons.append("High value product")

        # Late return
        if data["days_after_delivery"] > 10:
            score += 0.10
            reasons.append("Late return")

        # Product condition not sealed
        if data["product_condition"] != 0:
            score += 0.15
            reasons.append("Product not sealed")

        score = min(score, 1.0)

        # Map score to risk & decision
        if score >= 0.7:
            decision = "REJECT"
            risk = "HIGH"
        elif score >= 0.4:
            decision = "MANUAL REVIEW"
            risk = "MEDIUM"
        else:
            decision = "APPROVE"
            risk = "LOW"

        return {
            "fraud_score": round(score, 2),
            "risk": risk,
            "decision": decision,
            "explanation": reasons
        }

# Logistic Regression
lr_model = LogisticRegression(max_iter=2000)
lr_model.fit(X_train_sc, y_train)

# Random Forest
rf_model = RandomForestClassifier(n_estimators=100,random_state=42)
rf_model.fit(X_train_sc, y_train)


# SAVE MODELS AS PICKLES

models_folder = "ml/models/"
import os
os.makedirs(models_folder, exist_ok=True)

# Save rule-based engine
with open(f"{models_folder}rule_based.pkl", "wb") as f:
    pickle.dump(RuleBasedFraud(), f)

# Save ML models
with open(f"{models_folder}logistic_regression.pkl", "wb") as f:
    pickle.dump(lr_model, f)

with open(f"{models_folder}random_forest.pkl", "wb") as f:
    pickle.dump(rf_model, f)

print("Models saved in ml/models/ folder")


#CREATE CONFIG FOR ACTIVE MODEL

config = {
    "active_model": "rule_based.pkl"  # default active model
}

with open("ml/active_model.json", "w") as f:
    json.dump(config, f)

print("Active model set to rule-based by default")  