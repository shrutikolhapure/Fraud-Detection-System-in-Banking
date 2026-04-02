import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report

# ======================================================
# STEP 1: Create sample fraud dataset
# ======================================================

data = {
    "count": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
              11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    
    "type": [
        "TRANSFER", "TRANSFER", "CASH_OUT", "TRANSFER", "CASH_OUT",
        "TRANSFER", "CASH_OUT", "TRANSFER", "TRANSFER", "CASH_OUT",
        "TRANSFER", "TRANSFER", "CASH_OUT", "TRANSFER", "CASH_OUT",
        "TRANSFER", "CASH_OUT", "TRANSFER", "TRANSFER", "CASH_OUT"
    ],
    
    "amount": [
        500, 10000, 200, 50000, 100,
        7000, 300, 90000, 4500, 150,
        12000, 25000, 400, 80000, 250,
        15000, 350, 60000, 11000, 220
    ],
    
    "oldbalanceOrig": [
        10000, 15000, 5000, 60000, 3000,
        20000, 4500, 95000, 10000, 5000,
        18000, 30000, 6000, 90000, 4000,
        25000, 5500, 70000, 16000, 4500
    ],
    
    "newbalanceOrig": [
        9500, 5000, 4800, 10000, 2900,
        13000, 4200, 5000, 5500, 4850,
        6000, 5000, 5600, 10000, 3750,
        10000, 5150, 10000, 5000, 4280
    ],
    
    "oldbalanceDest": [
        2000, 3000, 1000, 5000, 1500,
        4000, 1200, 7000, 2500, 1100,
        3500, 4500, 1400, 6000, 1600,
        5000, 1800, 5500, 3700, 1300
    ],
    
    "newbalanceDest": [
        2500, 13000, 1200, 55000, 1600,
        11000, 1500, 97000, 7000, 1250,
        15500, 29500, 1800, 86000, 1850,
        20000, 2150, 65500, 14700, 1520
    ],
    
    # 0 = Genuine, 1 = Fraud
    "isFraud": [
        0, 0, 0, 1, 0,
        0, 0, 1, 0, 0,
        0, 1, 0, 1, 0,
        0, 0, 1, 0, 0
    ]
}

df = pd.DataFrame(data)

# ======================================================
# STEP 2: Separate features and target
# ======================================================

X = df.drop("isFraud", axis=1)
y = df["isFraud"]

# ======================================================
# STEP 3: Define preprocessing
# ======================================================

numeric_features = [
    "count", "amount", "oldbalanceOrig",
    "newbalanceOrig", "oldbalanceDest", "newbalanceDest"
]

categorical_features = ["type"]

numeric_transformer = Pipeline(steps=[
    ("scaler", MinMaxScaler())
])

categorical_transformer = Pipeline(steps=[
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# ======================================================
# STEP 4: Create full pipeline with model
# ======================================================

model_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])

# ======================================================
# STEP 5: Split data
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================================================
# STEP 6: Train model
# ======================================================

model_pipeline.fit(X_train, y_train)

# ======================================================
# STEP 7: Test model
# ======================================================

y_pred = model_pipeline.predict(X_test)

print("Model Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ======================================================
# STEP 8: Save model
# ======================================================

joblib.dump(model_pipeline, "banking_app_rf.pkl")

print("\n✅ banking_app_rf.pkl created successfully!")
