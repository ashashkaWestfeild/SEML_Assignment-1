import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train_baseline_model():
    print("[STEP 1] Training baseline Random Forest Classifier for Loan Approval Risk...")
    
    # Load dataset
    data_path = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\data\loan_data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Define features and label
    features = [
        'age', 'annual_income', 'credit_score', 'loan_amount', 
        'loan_duration', 'savings_balance', 'total_assets', 
        'total_liabilities', 'previous_defaults', 'cc_utilization'
    ]
    X = df[features]
    y = df['loan_approved']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train
    model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    model.fit(X_train, y_train)
    
    # Predict
    preds = model.predict(X_test)
    
    print("\nAccuracy Score:", accuracy_score(y_test, preds))
    print("\nClassification Report:")
    print(classification_report(y_test, preds))
    
    # Save model
    model_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\app"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.pkl")
    joblib.dump(model, model_path)
    print(f"\nModel saved successfully at {model_path}")

if __name__ == "__main__":
    train_baseline_model()
