import pandas as pd
import requests
import os
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

def main():
    # 1. Download Kaggle Dataset (Airline Satisfaction subset mapped to our features)
    url = "https://raw.githubusercontent.com/saulventura/Airline-Passenger-Satisfaction/master/train.csv"
    print("Downloading professional Kaggle dataset mirror...")
    df = pd.read_csv(url)

    # 2. Map columns to our 5 project features
    feature_mapping = {
        'Inflight service': 'service',
        'Seat comfort': 'product',
        'Checkin service': 'delivery',
        'On-board service': 'support',
        'Cleanliness': 'price',
        'satisfaction': 'satisfaction'
    }
    df_mapped = df[list(feature_mapping.keys())].rename(columns=feature_mapping)

    # Handle missing values
    df_mapped.dropna(inplace=True)

    # 3. Process Target to match UI predictions
    df_mapped['satisfaction'] = df_mapped['satisfaction'].map({
        'satisfied': 'Satisfied',
        'neutral or dissatisfied': 'Not Satisfied'
    })

    print("Dataset Sample:")
    print(df_mapped.head())
    print("\nClass Distribution Before SMOTE:")
    print(df_mapped['satisfaction'].value_counts())

    # Save to dataset/customer_satisfaction.csv
    os.makedirs("dataset", exist_ok=True)
    df_mapped.to_csv("dataset/customer_satisfaction.csv", index=False)
    print("Saved dataset to dataset/customer_satisfaction.csv")

    # 4. Train Model professionally
    X = df_mapped.drop('satisfaction', axis=1)
    y = df_mapped['satisfaction']

    # Use SMOTE to balance the dataset professionally
    smote = SMOTE(random_state=42)
    X_res, y_res = smote.fit_resample(X, y)
    
    print("\nClass Distribution After SMOTE:")
    print(y_res.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

    print("\nTraining Professional CatBoostClassifier...")
    model = CatBoostClassifier(iterations=300, learning_rate=0.05, depth=6, verbose=50)
    model.fit(X_train, y_train, eval_set=(X_test, y_test))

    # 5. Evaluate
    y_pred = model.predict(X_test)
    print("\nClassification Report on Test Data:")
    print(classification_report(y_test, y_pred))

    # 6. Save Model
    os.makedirs("model", exist_ok=True)
    model.save_model("model/catboost_model.cbm")
    print("Professional Model successfully trained and saved to model/catboost_model.cbm")

if __name__ == "__main__":
    main()
