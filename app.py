from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db_connection
from ml_service import predict_fraud

app = Flask(__name__)
CORS(app)

# ---------------- ADMIN SETTINGS ----------------
@app.route("/api/admin/settings", methods=["POST"])
def save_admin_settings():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO admin_settings
        (company_name, platform_id, risk_tolerance, fraud_threshold, auto_approve)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["company_name"],
        data["platform_id"],
        data["risk_tolerance"],
        data["fraud_threshold"],
        data["auto_approve"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Settings saved"}), 201


# ---------------- RETURN EVALUATION ----------------
@app.route("/api/evaluate-return", methods=["POST"])
def evaluate_return():
    data = request.json

    result = predict_fraud(data)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO return_requests
        (user_id, account_age, total_orders, total_returns, product_price,
         days_after_delivery, product_condition, high_value,
         pickup_changed, repeated_reason, product_category,
         fraud_score, risk_level, decision)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["user_id"],
        data["account_age"],
        data["total_orders"],
        data["total_returns"],
        data["product_price"],
        data["days_after_delivery"],
        data["product_condition"],
        data["high_value"],
        data["pickup_changed"],
        data["repeated_reason"],
        data["product_category"],
        result["fraud_score"],
        result["risk_level"],
        result["decision"]
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify(result)


# ---------------- HEALTH CHECK ----------------
@app.route("/")
def health():
    return "Backend running successfully 🚀"


if __name__ == "_main_":
    app.run(debug=True)