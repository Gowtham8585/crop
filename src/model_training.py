import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_crop_model(data_path='crop_recommendation.csv', model_path='models/crop_recommendation_model.pkl'):
    if not os.path.exists('models'):
        os.makedirs('models')
        
    # Load dataset
    df = pd.read_csv(data_path)
    
    # Preprocessing
    # Assuming the synthetic data is clean. Real data would need NaNs handled.
    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    
    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Model Initialization
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    
    # Training
    print("Training Random Forest Scheme...")
    rf.fit(X_train, y_train)
    
    # Evaluation
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {acc*100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    # Save Model
    joblib.dump(rf, model_path)
    print(f"Model saved to {model_path}")
    
    return rf, acc

if __name__ == "__main__":
    train_crop_model()
