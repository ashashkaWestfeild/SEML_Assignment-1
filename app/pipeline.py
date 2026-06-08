import time
import numpy as np
from app.schemas import LoanApplicationInput, LoanApprovalResult
from app.config import settings

# =========================================================
# FILTER 1 : INPUT VALIDATION FILTER
# Business-rule validation checks on raw input
# Quality Attribute: Robustness
# =========================================================
def validate_input(app_input: LoanApplicationInput) -> LoanApplicationInput:
    # Business level constraint checks that might not be covered by simple schema types
    if app_input.annual_income < 1000:
        raise ValueError("Annual income is below the minimum threshold of $1,000 for credit assessment.")
        
    if app_input.loan_amount > app_input.annual_income * 5:
        # Business rule: loan amount shouldn't exceed 5 times the annual income
        raise ValueError("Requested loan amount exceeds 500% of the applicant's annual income.")
        
    return app_input

# =========================================================
# FILTER 2 : FEATURE EXTRACTION FILTER
# Extract and normalize features, compute derivatives
# Quality Attribute: Maintainability
# =========================================================
def extract_features(app_input: LoanApplicationInput) -> tuple:
    # Deriving custom financial metrics
    net_worth = float(app_input.total_assets - app_input.total_liabilities)
    debt_to_income = float(app_input.total_liabilities / (app_input.annual_income + 1e-5))
    
    # Building ordered numpy array for model input matching training columns
    feature_vector = np.array([[
        app_input.age,
        app_input.annual_income,
        app_input.credit_score,
        app_input.loan_amount,
        app_input.loan_duration,
        app_input.savings_balance,
        app_input.total_assets,
        app_input.total_liabilities,
        app_input.previous_defaults,
        app_input.cc_utilization
    ]], dtype=float)
    
    return feature_vector, net_worth, debt_to_income

# =========================================================
# FILTER 3 : MODEL RUNNING FILTER
# Run classification inference using the trained Random Forest model
# Quality Attribute: Performance
# =========================================================
def run_model(feature_vector: np.ndarray, model) -> tuple:
    # Model inference
    # Predict probabilities (index 1 is probability of approval)
    probabilities = model.predict_proba(feature_vector)[0]
    prob_approved = float(probabilities[1])
    
    # Binary threshold decisioning
    is_approved = prob_approved >= settings.DEFAULT_DECISION_THRESHOLD
    
    return is_approved, prob_approved

# =========================================================
# FILTER 4 : RESPONSE FORMATTER FILTER
# Determine risk tiering and construct output schema
# Quality Attribute: Reliability
# =========================================================
def format_response(
    is_approved: bool, 
    prob: float, 
    net_worth: float, 
    debt_to_income: float, 
    previous_defaults: int,
    latency_ms: float
) -> LoanApprovalResult:
    # Categorizing into risk tiers
    if prob >= 0.70 and previous_defaults == 0:
        risk_tier = "LOW"
    elif prob >= 0.40 and previous_defaults == 0:
        risk_tier = "MEDIUM"
    else:
        risk_tier = "HIGH"
        
    # Build Pydantic output model
    result = LoanApprovalResult(
        is_approved=is_approved,
        probability=round(prob, 4),
        risk_tier=risk_tier,
        net_worth=round(net_worth, 2),
        debt_to_income=round(debt_to_income, 4),
        latency_ms=round(latency_ms, 2)
    )
    return result

# =========================================================
# PIPELINE EXECUTION (PIPE CONNECTING FILTERS)
# =========================================================
def execute_pipeline(app_input: LoanApplicationInput, model) -> LoanApprovalResult:
    start_time = time.perf_counter()
    
    # Stage 1: Validation (Filter 1)
    validated_input = validate_input(app_input)
    
    # Stage 2: Feature Extraction (Filter 2)
    features, net_worth, debt_to_income = extract_features(validated_input)
    
    # Stage 3: Inference (Filter 3)
    is_approved, prob = run_model(features, model)
    
    # Calculate latency before format step
    latency_ms = (time.perf_counter() - start_time) * 1000.0
    
    # Stage 4: Formatting (Filter 4)
    result = format_response(
        is_approved, 
        prob, 
        net_worth, 
        debt_to_income, 
        validated_input.previous_defaults, 
        latency_ms
    )
    return result
