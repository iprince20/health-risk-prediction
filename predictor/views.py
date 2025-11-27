from django.shortcuts import render
import joblib
import pandas as pd
import os

# Absolute path to the model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "predictor", "best_health_risk_model.pkl")

model = joblib.load(MODEL_PATH)
# Feature order
feature_cols = [
    "age",
    "gender",
    "heart_rate_bpm",
    "systolic_bp",
    "diastolic_bp",
    "temperature_c",
    "spo2_percent",
    "bmi",
    "has_diabetes",
    "smoker",
]

# Validation
def validate_patient_data(data):
    for key, value in data.items():
        if value is None or value == "":
            return False, f"{key} is missing."

        try:
            float(value)
        except:
            return False, f"{key} must be a number."

    if float(data["gender"]) not in [0, 1]:
        return False, "Gender must be 0 or 1."
    if float(data["has_diabetes"]) not in [0, 1]:
        return False, "Has Diabetes must be 0 or 1."
    if float(data["smoker"]) not in [0, 1]:
        return False, "Smoker must be 0 or 1."

    return True, "OK"


# MAIN VIEW
def home(request):
    prediction = None
    error = None

    if request.method == "POST":
        patient_data = {key: request.POST.get(key) for key in feature_cols}

        is_valid, message = validate_patient_data(patient_data)
        if not is_valid:
            error = message
        else:
            clean_data = {k: float(v) for k, v in patient_data.items()}
            X_new = pd.DataFrame([clean_data], columns=feature_cols)

            pred_class = model.predict(X_new)[0]

            label_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
            prediction = label_map.get(int(pred_class), "Unknown")

    return render(request, "predictor/form.html", {
        "prediction": prediction,
        "error": error
    })
