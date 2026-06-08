import time
import unittest
import numpy as np
import joblib
from pydantic import ValidationError

from app.schemas import LoanApplicationInput, LoanApprovalResult
from app.config import settings
from app.pipeline import validate_input, extract_features, run_model, format_response, execute_pipeline

class TestQualityAttributes(unittest.TestCase):

    def setUp(self):
        self.sample_valid_input = LoanApplicationInput(
            age=35,
            annual_income=75000.0,
            credit_score=720,
            loan_amount=20000.0,
            loan_duration=36,
            savings_balance=15000.0,
            total_assets=120000.0,
            total_liabilities=40000.0,
            previous_defaults=0,
            cc_utilization=0.25
        )
        self.model = joblib.load(settings.MODEL_PATH)

    # =========================================================
    # QUALITY ATTRIBUTE: ROBUSTNESS
    # Verifying that invalid data is rejected at the API schema boundaries
    # =========================================================
    def test_schema_rejects_low_age(self):
        with self.assertRaises(ValidationError):
            # Under 18 is not allowed
            LoanApplicationInput(
                age=17, annual_income=50000, credit_score=600, loan_amount=1000,
                loan_duration=24, savings_balance=100, total_assets=100,
                total_liabilities=0, previous_defaults=0, cc_utilization=0.1
            )
            
    def test_schema_rejects_invalid_credit_score(self):
        with self.assertRaises(ValidationError):
            # Credit score > 850 is invalid
            LoanApplicationInput(
                age=30, annual_income=50000, credit_score=900, loan_amount=1000,
                loan_duration=24, savings_balance=100, total_assets=100,
                total_liabilities=0, previous_defaults=0, cc_utilization=0.1
            )
            
    def test_pipeline_rejects_excessive_loan_ratio(self):
        # Exceeds 5 times annual income (500%)
        self.sample_valid_input.loan_amount = 400000.0
        self.sample_valid_input.annual_income = 50000.0
        
        with self.assertRaises(ValueError):
            validate_input(self.sample_valid_input)

    # =========================================================
    # QUALITY ATTRIBUTE: RELIABILITY
    # Verifying schema validation consistency and well-formed outputs
    # =========================================================
    def test_pipeline_output_conforms_to_schema(self):
        result = execute_pipeline(self.sample_valid_input, self.model)
        self.assertIsInstance(result, LoanApprovalResult)
        self.assertIsInstance(result.is_approved, bool)
        self.assertTrue(0.0 <= result.probability <= 1.0)
        self.assertIn(result.risk_tier, ["LOW", "MEDIUM", "HIGH"])
        self.assertEqual(result.net_worth, self.sample_valid_input.total_assets - self.sample_valid_input.total_liabilities)
        self.assertTrue(result.debt_to_income >= 0.0)

    # =========================================================
    # QUALITY ATTRIBUTE: PERFORMANCE
    # Verifying inference latency meets SLA guidelines (Latency < 200ms)
    # =========================================================
    def test_inference_pipeline_latency(self):
        # Warmup
        _ = execute_pipeline(self.sample_valid_input, self.model)
        
        latencies = []
        for _ in range(50):
            t_start = time.perf_counter()
            _ = execute_pipeline(self.sample_valid_input, self.model)
            t_end = time.perf_counter()
            latencies.append((t_end - t_start) * 1000.0)
            
        avg_latency = sum(latencies) / len(latencies)
        print(f"\n[PERFORMANCE] Average Pipeline Execution Latency: {avg_latency:.4f} ms")
        
        # Performance assertion
        self.assertTrue(avg_latency < 200.0, f"Average latency ({avg_latency:.2f} ms) exceeds SLA limit of 200ms")

    # =========================================================
    # QUALITY ATTRIBUTE: MAINTAINABILITY
    # Verifying pipeline stages are pure functions and isolated
    # =========================================================
    def test_validation_filter_is_pure(self):
        input_copy = self.sample_valid_input.model_copy()
        output = validate_input(self.sample_valid_input)
        
        # Output should be the same as input
        self.assertEqual(output.annual_income, input_copy.annual_income)
        # Input object shouldn't be mutated
        self.assertEqual(self.sample_valid_input, input_copy)
        
    def test_feature_extraction_filter_isolation(self):
        features, net_worth, dti = extract_features(self.sample_valid_input)
        
        self.assertIsInstance(features, np.ndarray)
        self.assertEqual(features.shape, (1, 10))
        self.assertEqual(net_worth, self.sample_valid_input.total_assets - self.sample_valid_input.total_liabilities)
        self.assertEqual(dti, self.sample_valid_input.total_liabilities / (self.sample_valid_input.annual_income + 1e-5))

if __name__ == "__main__":
    unittest.main()
