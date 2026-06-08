import os
import yaml

class Settings:
    def __init__(self):
        self.PROJECT_NAME = "Loan Approval Risk Service"
        self.APP_ENV = "production"
        self.MODEL_PATH = "app/model.pkl"
        self.DEFAULT_DECISION_THRESHOLD = 0.50
        self.LOG_LEVEL = "INFO"
        self.FEATURES = []
        
        # Load from config.yaml if available
        base_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1"
        config_path = os.path.join(base_dir, "configs", "config.yaml")
        
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    self.PROJECT_NAME = config['app']['name']
                    self.APP_ENV = config['app']['env']
                    self.MODEL_PATH = os.path.join(base_dir, config['model']['path'])
                    self.DEFAULT_DECISION_THRESHOLD = float(config['model']['default_threshold'])
                    self.FEATURES = config['model']['features']
                    self.LOG_LEVEL = config['logging']['level']
                    print(f"Configurations loaded successfully from {config_path}")
            except Exception as e:
                print(f"[WARNING] Failed to parse config.yaml, using defaults. Error: {str(e)}")
        else:
            print(f"[WARNING] config.yaml not found at {config_path}, using code defaults.")
            # Fallback defaults
            self.MODEL_PATH = os.path.join(base_dir, "app", "model.pkl")
            self.FEATURES = [
                'age', 'annual_income', 'credit_score', 'loan_amount', 
                'loan_duration', 'savings_balance', 'total_assets', 
                'total_liabilities', 'previous_defaults', 'cc_utilization'
            ]

settings = Settings()
