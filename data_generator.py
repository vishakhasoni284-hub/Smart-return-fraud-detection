import pandas as pd
import numpy as np

np.random.seed(42)
rows = 1000

data = {
    "account_age_days": np.random.randint(10, 2000, rows),
    "total_orders": np.random.randint(1, 50, rows),
    "total_returns": np.random.randint(0, 20, rows),
    "product_price": np.random.randint(100, 10000, rows),
    "days_after_delivery": np.random.randint(1, 30, rows),
    "product_condition": np.random.choice(["Sealed", "Opened", "Damaged"], rows),
    "high_value_product": np.random.choice([0, 1], rows),
    "pickup_location_changed": np.random.choice([0, 1], rows),
    "repeated_return_reason": np.random.choice([0, 1], rows),
    "product_category": np.random.choice(["Electronics","Clothing","Footwear","Accessories"], rows)
}

df = pd.DataFrame(data)


df["is_fraud"] = (
    (df["total_returns"] / np.maximum(df["total_orders"], 1) > 0.5).astype(int) +
    (df["account_age_days"] < 100).astype(int) +
    (df["product_price"] > 3000).astype(int) +
    (df["days_after_delivery"] > 10).astype(int) +
    (df["product_condition"] != "Sealed").astype(int)
)

# If 2 or more signals -> fraud
df["is_fraud"] = (df["is_fraud"] >= 2).astype(int)


df.to_csv("ml/returns_data.csv", index=False)
print("Dataset generated")