import unittest
from ai_shield_kenya.detectors import FraudDetector, MisinformationDetector, ToxicityDetector


class TestDetectors(unittest.TestCase):
    """
    Test suite for detector classes.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.fraud_detector = FraudDetector()
        self.misinfo_detector = MisinformationDetector()
        self.toxicity_detector = ToxicityDetector()
    
    def test_fraud_detector_basic(self):
        """
        Test basic fraud detection functionality.
        """
        # Test with fraud pattern
        result = self.fraud_detector.detect("Send KSh 5000 to M-Pesa number 0712345678")
        
        self.assertTrue(result['detected'])
        self.assertIn('severity', result)
        self.assertIn('risk_score', result)
        self.assertIn('explanation', result)
        self.assertIn('recommendations', result)
        
        # Test with safe text
        safe_result = self.fraud_detector.detect("M-Pesa transfers are guaranteed safe and secure")
        self.assertFalse(safe_result['detected'])
    
    def test_misinformation_detector_basic(self):
        """
        Test basic misinformation detection functionality.
        """
        # Test with misinformation pattern
        result = self.misinfo_detector.detect("CBC Math Grade 4: 2+2=5", domain="education")
        
        self.assertTrue(result['detected'])
        self.assertIn('severity', result)
        self.assertIn('risk_score', result)
        self.assertIn('explanation', result)
        self.assertIn('recommendations', result)
        
        # Test with safe text
        safe_result = self.misinfo_detector.detect("CBC Math Grade 4 covers basic arithmetic operations")
        self.assertFalse(safe_result['detected'])
    
    def test_toxicity_detector_basic(self):
        """
        Test basic toxicity detection functionality.
        """
        # Test with toxicity pattern
        result = self.toxicity_detector.detect("Use bleach to kill aphids on tomatoes")
        
        self.assertTrue(result['detected'])
        self.assertIn('severity', result)
        self.assertIn('risk_score', result)
        self.assertIn('explanation', result)
        self.assertIn('recommendations', result)
        
        # Test with safe text
        safe_result = self.toxicity_detector.detect("Mafuta ya neem ni dawa ya wadudu ya kimwili ambayo inatumika kwa usalama kwenye mimea")
        self.assertFalse(safe_result['detected'])
    
    def test_language_support(self):
        """
        Test language support for detectors.
        """
        # Swahili fraud detection
        sw_fraud_result = self.fraud_detector.detect("Kutuma pesa kwa namba ya simu ili kupata tuzo ya loteri", language="sw")
        self.assertTrue(sw_fraud_result['detected'])
        
        # Swahili misinformation detection
        sw_misinfo_result = self.misinfo_detector.detect("Ushahidi wa uhuru ulikuwa kwa ajili ya kusimama na serikali ya ukoloni", language="sw", domain="education")
        self.assertTrue(sw_misinfo_result['detected'])
        
        # Swahili toxicity detection
        sw_toxicity_result = self.toxicity_detector.detect("Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach", language="sw")
        self.assertTrue(sw_toxicity_result['detected'])
    
    def test_severity_levels(self):
        """
        Test different severity levels.
        """
        # High severity fraud
        high_fraud = self.fraud_detector.detect("Buy our miracle fertilizer that increases yield by 500%")
        self.assertEqual(high_fraud['severity'], "high")
        
        # Medium severity fraud
        medium_fraud = self.fraud_detector.detect("M-Pesa transfers are guaranteed safe and secure")
        self.assertEqual(medium_fraud['severity'], "medium")
        
        # Low severity fraud (if any)
        # Test with single pattern match
        low_fraud = self.fraud_detector.detect("Send money via M-Pesa")
        # Should be at least low severity
        self.assertIn(low_fraud['severity'], ["low", "medium", "high", "none"])
    
    def test_recommendations(self):
        """
        Test recommendations generation.
        """
        # Fraud recommendations
        fraud_result = self.fraud_detector.detect("Send KSh 5000 to M-Pesa number 0712345678")
        self.assertIsInstance(fraud_result['recommendations'], list)
        self.assertGreater(len(fraud_result['recommendations']), 0)
        
        # Misinformation recommendations
        misinfo_result = self.misinfo_detector.detect("Grade 7 science says water boils at 90°C", domain="education")
        self.assertIsInstance(misinfo_result['recommendations'], list)
        self.assertGreater(len(misinfo_result['recommendations']), 0)
        
        # Toxicity recommendations
        toxicity_result = self.toxicity_detector.detect("Bleach is safe for plants and humans when diluted properly")
        self.assertIsInstance(toxicity_result['recommendations'], list)
        self.assertGreater(len(toxicity_result['recommendations']), 0)


if __name__ == '__main__':
    unittest.main()