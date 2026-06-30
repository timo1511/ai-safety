import unittest
import numpy as np
from ai_shield_kenya.sir_model import SIRHarmModel


class TestSIRHarmModel(unittest.TestCase):
    """
    Test suite for SIRHarmModel class.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.model = SIRHarmModel(beta=0.5, gamma=0.1)
    
    def test_initialization(self):
        """
        Test that model initializes with correct parameters.
        """
        self.assertEqual(self.model.beta, 0.5)
        self.assertEqual(self.model.gamma, 0.1)
        self.assertFalse(self.model.fitted)
    
    def test_sir_equations(self):
        """
        Test the SIR differential equations implementation.
        """
        # Test with simple values
        y = [100.0, 10.0, 0.0]  # S, I, R
        t = 0.0
        beta = 0.5
        gamma = 0.1
        N = 110.0
        
        result = self.model._sir_equations(y, t, beta, gamma, N)
        
        # Calculate expected values manually
        dS_dt = -beta * y[0] * y[1] / N
        dI_dt = beta * y[0] * y[1] / N - gamma * y[1]
        dR_dt = gamma * y[1]
        
        self.assertAlmostEqual(result[0], dS_dt, places=6)
        self.assertAlmostEqual(result[1], dI_dt, places=6)
        self.assertAlmostEqual(result[2], dR_dt, places=6)
    
    def test_predict_basic(self):
        """
        Test basic prediction functionality.
        """
        # Fit the model first
        training_data = [{"harm_level": 50, "context_complexity": 100}]
        self.model.fit(training_data)
        
        # Make prediction
        result = self.model.predict("Test prompt")
        
        # Check structure
        self.assertIn('trajectory', result)
        self.assertIn('peak_infection', result)
        self.assertIn('final_infection', result)
        self.assertIn('recovery_rate', result)
        self.assertIn('risk_probability', result)
        
        # Check data types
        self.assertIsInstance(result['peak_infection'], float)
        self.assertIsInstance(result['final_infection'], float)
        self.assertIsInstance(result['recovery_rate'], float)
        self.assertIsInstance(result['risk_probability'], float)
    
    def test_score_risk(self):
        """
        Test risk scoring functionality.
        """
        # Fit the model first
        training_data = [{"harm_level": 50, "context_complexity": 100}]
        self.model.fit(training_data)
        
        # Score risk
        risk_score = self.model.score_risk("Test prompt", context_complexity=100)
        
        # Check range
        self.assertGreaterEqual(risk_score, 0.0)
        self.assertLessEqual(risk_score, 100.0)
        self.assertIsInstance(risk_score, float)
    
    def test_get_parameters(self):
        """
        Test parameter retrieval.
        """
        params = self.model.get_parameters()
        self.assertEqual(params['beta'], 0.5)
        self.assertEqual(params['gamma'], 0.1)
    
    def test_numerical_stability(self):
        """
        Test model stability with edge cases.
        """
        # Test with empty string
        result = self.model.predict("")
        self.assertIsInstance(result['risk_probability'], float)
        
        # Test with very short text
        result = self.model.predict("a")
        self.assertIsInstance(result['risk_probability'], float)
        
        # Test with very long text
        long_text = "a" * 1000
        result = self.model.predict(long_text)
        self.assertIsInstance(result['risk_probability'], float)


if __name__ == '__main__':
    unittest.main()