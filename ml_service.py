import pickle
import json

def load_active_model():
    with open("../ML/active-model.json") as f:
        active_model = json.load(f)["active_model"]

    model_path = f"../ML/models/{active_model}.pkl"
    with open(model_path, "rb") as f:
        return pickle.load(f)

def predict_fraud(data):
    model = load_active_model()
    return model.predict(data)