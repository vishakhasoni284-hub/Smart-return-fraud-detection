import pickle
import json
import os
import numpy as np

BASE_DIR = os.path.dirname(__file__)

def load_active_model():
    with open(os.path.join(BASE_DIR, "active_model.json")) as f:
        active_model = json.load(f)["active_model"]

    model_path = os.path.join(BASE_DIR, "ml/models", active_model)
    with open(model_path, "rb") as f:
        return pickle.load(f)


def predict_fraud(data):
    model = load_active_model()

    # RULE BASED MODEL
    if hasattr(model, "predict") and not hasattr(model, "predict_proba"):
        return model.predict(data)

    # ML MODEL
    features = np.array([[
        data["account_age"],
        data["total_orders"],
        data["total_returns"],
        data["product_price"],
        data["days_after_delivery"],
        0,  # encoded product_condition placeholder
        int(data["high_value"]),
        int(data["pickup_changed"]),
        int(data["repeated_reason"]),
        0   # encoded product_category placeholder
    ]])

    pred = model.predict(features)[0]
    score = float(model.predict_proba(features)[0][1])

    return {
        "fraud_score": round(score, 2),
        "risk_level": "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW",
        "decision": "REJECT" if score > 0.7 else "MANUAL_REVIEW" if score > 0.4 else "APPROVE",
        "explanation": ["ML model prediction"]
    }
