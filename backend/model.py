import os
import joblib
import numpy as np
import pandas as pd

from xgboost import XGBClassifier

from features import get_model_features


# --------------------------------------------------
# Model location
# --------------------------------------------------

MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "model"
)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "weather_model.pkl"
)


# --------------------------------------------------
# Features used by the model
# --------------------------------------------------

MODEL_FEATURES = [
    "temperature",
    "humidity",
    "precipitation",
    "wind_speed",
    "wind_gust",
    "cloud_cover",
    "pressure",
    "vapour_pressure_deficit",
    "rain_3h",
    "rain_6h",
    "wind_change",
    "pressure_change",
    "humidity_change",
    "cloud_change",
]


# --------------------------------------------------
# Create synthetic training data
# --------------------------------------------------

def create_training_data(n_samples=5000):

    np.random.seed(42)

    data = pd.DataFrame({

        "temperature": np.random.normal(
            28, 5, n_samples
        ),

        "humidity": np.random.uniform(
            40, 100, n_samples
        ),

        "precipitation": np.random.exponential(
            3, n_samples
        ),

        "wind_speed": np.random.uniform(
            0, 50, n_samples
        ),

        "wind_gust": np.random.uniform(
            0, 80, n_samples
        ),

        "cloud_cover": np.random.uniform(
            0, 100, n_samples
        ),

        "pressure": np.random.normal(
            1005, 10, n_samples
        ),

        "vapour_pressure_deficit": np.random.uniform(
            0, 5, n_samples
        ),

        "rain_3h": np.random.exponential(
            8, n_samples
        ),

        "rain_6h": np.random.exponential(
            15, n_samples
        ),

        "wind_change": np.random.normal(
            0, 8, n_samples
        ),

        "pressure_change": np.random.normal(
            0, 5, n_samples
        ),

        "humidity_change": np.random.normal(
            0, 8, n_samples
        ),

        "cloud_change": np.random.normal(
            0, 15, n_samples
        ),
    })


    # --------------------------------------------------
    # Create a simple prototype risk score
    # --------------------------------------------------

    risk_score = (

        0.03 * data["humidity"]

        + 0.15 * data["precipitation"]

        + 0.08 * data["wind_speed"]

        + 0.06 * data["wind_gust"]

        + 0.02 * data["cloud_cover"]

        + 0.20 * data["rain_3h"]

        + 0.12 * data["rain_6h"]

        - 0.10 * data["pressure"]

        + 0.10 * data["humidity_change"].clip(lower=0)

        + 0.05 * data["cloud_change"].clip(lower=0)

        - 0.05 * data["pressure_change"]
    )


    # --------------------------------------------------
    # Convert score into binary label
    # --------------------------------------------------

    threshold = risk_score.quantile(0.75)

    data["severe_weather"] = (
        risk_score > threshold
    ).astype(int)


    X = data[MODEL_FEATURES]

    y = data["severe_weather"]

    return X, y


# --------------------------------------------------
# Train model
# --------------------------------------------------

def train_model():

    print("Creating training data...")

    X, y = create_training_data()


    print("Training XGBoost model...")

    model = XGBClassifier(

        n_estimators=200,

        max_depth=5,

        learning_rate=0.05,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="binary:logistic",

        eval_metric="logloss",

        random_state=42
    )


    model.fit(X, y)


    # Create model directory
    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )


    # Save model
    joblib.dump(
        model,
        MODEL_PATH
    )


    print(
        f"Model saved to: {MODEL_PATH}"
    )


    return model


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

def load_model():

    if not os.path.exists(MODEL_PATH):

        print(
            "Model not found."
        )

        print(
            "Training a new model..."
        )

        return train_model()


    model = joblib.load(
        MODEL_PATH
    )

    return model


# --------------------------------------------------
# Predict severe weather risk
# --------------------------------------------------

def predict_risk(weather_data):

    model = load_model()


    # Convert raw weather data
    # into model features

    features = get_model_features(
        weather_data
    )


    # Take the latest observation

    latest_features = features.iloc[
        [-1]
    ]


    # Make prediction

    probability = model.predict_proba(
        latest_features
    )[0][1]


    probability = float(
        probability
    )


    # --------------------------------------------------
    # Convert probability to risk category
    # --------------------------------------------------

    if probability < 0.30:

        risk_level = "LOW"

    elif probability < 0.70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"


    return {

        "probability": round(
            probability * 100,
            2
        ),

        "risk_level": risk_level
    }


# --------------------------------------------------
# Test model directly
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "Training weather risk model..."
    )

    train_model()

    print(
        "Training completed."
    )