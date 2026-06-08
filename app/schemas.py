from pydantic import BaseModel, Field

class LoanApplicationInput(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Age of the applicant, must be between 18 and 100")
    annual_income: float = Field(..., gt=0, description="Applicant's yearly income, must be positive")
    credit_score: int = Field(..., ge=300, le=850, description="Credit score, must be between 300 and 850")
    loan_amount: float = Field(..., gt=0, description="Requested loan size, must be positive")
    loan_duration: int = Field(..., ge=12, le=60, description="Loan term in months, must be between 12 and 60")
    savings_balance: float = Field(..., ge=0, description="Savings account balance, cannot be negative")
    total_assets: float = Field(..., ge=0, description="Total assets value, cannot be negative")
    total_liabilities: float = Field(..., ge=0, description="Total liabilities value, cannot be negative")
    previous_defaults: int = Field(..., ge=0, le=1, description="Previous defaults status (0 for no, 1 for yes)")
    cc_utilization: float = Field(..., ge=0.0, le=1.0, description="Credit card utilization rate, between 0.0 and 1.0")

class LoanApprovalResult(BaseModel):
    is_approved: bool = Field(..., description="Binary classification outcome (True for approve, False for deny)")
    probability: float = Field(..., description="Calculated model probability of loan approval")
    risk_tier: str = Field(..., description="Categorized risk category: 'LOW', 'MEDIUM', or 'HIGH'")
    net_worth: float = Field(..., description="Calculated net worth (Assets - Liabilities)")
    debt_to_income: float = Field(..., description="Computed debt-to-income ratio")
    latency_ms: float = Field(..., description="API request processing time in milliseconds")
