import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Attempt to import mlflow
try:
    import mlflow
    import mlflow.sklearn
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    print("[WARNING] mlflow is not installed. Running in SIMULATED MLflow tracking mode.")

def train_with_mlflow(n_estimators=100, max_depth=6):
    print(f"\n[STEP 2] Training Model with MLflow Tracking (n_estimators={n_estimators}, max_depth={max_depth})...")
    
    # Load dataset
    data_path = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\data\loan_data.csv"
    df = pd.read_csv(data_path)
    
    features = [
        'age', 'annual_income', 'credit_score', 'loan_amount', 
        'loan_duration', 'savings_balance', 'total_assets', 
        'total_liabilities', 'previous_defaults', 'cc_utilization'
    ]
    X = df[features]
    y = df['loan_approved']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    
    params = {
        'n_estimators': n_estimators,
        'max_depth': max_depth,
        'random_state': 42
    }
    
    if MLFLOW_AVAILABLE:
        mlflow.set_experiment('loan_approval_risk_experiment')
        with mlflow.start_run():
            # Log params
            mlflow.log_params(params)
            
            # Fit
            model.fit(X_train, y_train)
            
            # Predict & Evaluate
            preds = model.predict(X_test)
            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds)
            rec = recall_score(y_test, preds)
            f1 = f1_score(y_test, preds)
            
            metrics = {
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1_score': f1
            }
            
            # Log metrics
            mlflow.log_metrics(metrics)
            
            # Log model
            mlflow.sklearn.log_model(model, 'loan_risk_model')
            
            print("Successfully logged run details, params, metrics and model artifact to MLflow Server.")
            print("Logged Params:", params)
            print("Logged Metrics:", metrics)
    else:
        # Simulated MLflow tracking (prints to console, logs to file)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds)
        rec = recall_score(y_test, preds)
        f1 = f1_score(y_test, preds)
        
        metrics = {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1_score': f1
        }
        
        print("--- SIMULATED MLFLOW LOGGING ---")
        print(f"Setting experiment: 'loan_approval_risk_experiment'")
        print(f"Active Run started.")
        print(f"Logged Parameter: n_estimators -> {n_estimators}")
        print(f"Logged Parameter: max_depth -> {max_depth}")
        print(f"Logged Metric: accuracy -> {acc:.4f}")
        print(f"Logged Metric: precision -> {prec:.4f}")
        print(f"Logged Metric: recall -> {rec:.4f}")
        print(f"Logged Metric: f1_score -> {f1:.4f}")
        print(f"Logged Artifact: sklearn model -> 'loan_risk_model.pkl'")
        print("Active Run ended.")
        print("--------------------------------")
        
    # Overwrite production model in app directory
    model_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\app"
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, os.path.join(model_dir, "model.pkl"))
    print(f"Model saved successfully to {os.path.join(model_dir, 'model.pkl')}")

if __name__ == "__main__":
    train_with_mlflow(n_estimators=150, max_depth=6)
