import os
import numpy as np
import pandas as pd

def generate_loan_data(num_records=5000, random_seed=42):
    np.random.seed(random_seed)
    
    # 1. Demographic & Basic Financials
    age = np.random.randint(18, 76, size=num_records)
    annual_income = np.random.uniform(15000, 180000, size=num_records).round(2)
    
    # 2. Credit Profile
    # Credit score normally distributed around 650, clipped between 300 and 850
    credit_score = np.random.normal(loc=650, scale=100, size=num_records).astype(int)
    credit_score = np.clip(credit_score, 300, 850)
    
    # 3. Requested Loan Details
    # Loan amount depends loosely on income
    loan_amount = (annual_income * np.random.uniform(0.1, 0.6, size=num_records)).round(2)
    loan_duration = np.random.choice([12, 24, 36, 48, 60], size=num_records)
    
    # 4. Assets & Liabilities
    savings_balance = (annual_income * np.random.uniform(0.05, 0.8, size=num_records)).round(2)
    total_assets = (annual_income * np.random.uniform(0.5, 4.0, size=num_records)).round(2)
    total_liabilities = (annual_income * np.random.uniform(0.1, 1.5, size=num_records)).round(2)
    
    # 5. Risk indicators
    previous_defaults = np.random.choice([0, 1], size=num_records, p=[0.88, 0.12])
    cc_utilization = np.random.uniform(0.0, 1.0, size=num_records).round(4)
    
    # 6. Target Generation Heuristic (LoanApproved: 0 or 1)
    # Calculate a custom "approval score" based on risk rules
    approval_prob = []
    for i in range(num_records):
        score = 0.5 # Baseline probability
        
        # Credit Score effect
        if credit_score[i] >= 720:
            score += 0.3
        elif credit_score[i] < 580:
            score -= 0.3
            
        # Default effect
        if previous_defaults[i] == 1:
            score -= 0.4
            
        # Assets & Liabilities ratio
        asset_ratio = total_assets[i] / (total_liabilities[i] + 1)
        if asset_ratio > 3.0:
            score += 0.15
        elif asset_ratio < 1.0:
            score -= 0.15
            
        # Savings effect
        if savings_balance[i] > (loan_amount[i] * 0.5):
            score += 0.15
            
        # CC Utilization effect
        if cc_utilization[i] > 0.7:
            score -= 0.15
        elif cc_utilization[i] < 0.3:
            score += 0.1
            
        # Income to Loan Amount ratio
        income_to_loan = annual_income[i] / loan_amount[i]
        if income_to_loan < 2.0:
            score -= 0.2
            
        # Final probability bounded between 0 and 1
        prob = np.clip(score, 0.01, 0.99)
        approval_prob.append(prob)
        
    loan_approved = np.random.binomial(1, approval_prob)
    
    df = pd.DataFrame({
        'age': age,
        'annual_income': annual_income,
        'credit_score': credit_score,
        'loan_amount': loan_amount,
        'loan_duration': loan_duration,
        'savings_balance': savings_balance,
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'previous_defaults': previous_defaults,
        'cc_utilization': cc_utilization,
        'loan_approved': loan_approved
    })
    
    # Save to CSV
    data_dir = r"c:\Users\singh\OneDrive\Documents\BITS WILP\Sem 2\SEML\SEML Assignment 1\data"
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "loan_data.csv"), index=False)
    print(f"Generated synthetic loan dataset with {num_records} rows at {os.path.join(data_dir, 'loan_data.csv')}")
    print(df['loan_approved'].value_counts())

if __name__ == "__main__":
    generate_loan_data()
