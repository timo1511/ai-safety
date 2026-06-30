import unittest
from ai_shield_kenya.risk_scorer import RiskScorer


class TestRiskScorer(unittest.TestCase):
    """
    Test suite for RiskScorer class.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.scorer = RiskScorer()
    
    def test_score_basic(self):
        """
        Test basic scoring functionality.
        """
        result = self.scorer.score("Test prompt")
        
        # Check structure
        self.assertIn('risk_score', result)
        self.assertIn('category', result)
        self.assertIn('suggestion', result)
        self.assertIn('language', result)
        self.assertIn('domain', result)
        
        # Check data types
        self.assertIsInstance(result['risk_score'], float)
        self.assertIsInstance(result['category'], str)
        self.assertIsInstance(result['suggestion'], str)
        self.assertIsInstance(result['language'], str)
        self.assertIsInstance(result['domain'], str)
        
        # Check range
        self.assertGreaterEqual(result['risk_score'], 0.0)
        self.assertLessEqual(result['risk_score'], 100.0)
    
    def test_score_language_variants(self):
        """
        Test scoring with different languages.
        """
        # English
        en_result = self.scorer.score("Use bleach to cure crop disease", language="en")
        self.assertEqual(en_result['language'], "en")
        
        # Swahili
        sw_result = self.scorer.score("Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach", language="sw")
        self.assertEqual(sw_result['language'], "sw")
        
        # Kisii
        ki_result = self.scorer.score("rie chira ni rieto", language="ki")
        self.assertEqual(ki_result['language'], "ki")
    
    def test_score_domains(self):
        """
        Test scoring with different domains.
        """
        # Agriculture
        agri_result = self.scorer.score("Use bleach to kill aphids on tomatoes", domain="agriculture")
        self.assertEqual(agri_result['domain'], "agriculture")
        
        # Education
        edu_result = self.scorer.score("CBC Math Grade 4: 2+2=5", domain="education")
        self.assertEqual(edu_result['domain'], "education")
        
        # General
        gen_result = self.scorer.score("Hello world", domain="general")
        self.assertEqual(gen_result['domain'], "general")
    
    def test_suggest_fixes(self):
        """
        Test suggest_fixes functionality.
        """
        # Fraud case
        fraud_result = self.scorer.suggest_fixes("Send money to unknown M-Pesa number")
        self.assertIsInstance(fraud_result, list)
        self.assertGreater(len(fraud_result), 0)
        
        # Misinformation case
        misinfo_result = self.scorer.suggest_fixes("2+2=5 is correct for CBC Grade 4")
        self.assertIsInstance(misinfo_result, list)
        self.assertGreater(len(misinfo_result), 0)
        
        # Toxicity case
        toxicity_result = self.scorer.suggest_fixes("Bleach is safe for plants when diluted")
        self.assertIsInstance(toxicity_result, list)
        self.assertGreater(len(toxicity_result), 0)
    
    def test_boundary_conditions(self):
        """
        Test boundary conditions and edge cases.
        """
        # Empty string
        empty_result = self.scorer.score("")
        self.assertIsInstance(empty_result['risk_score'], float)
        
        # Very long text
        long_text = "a" * 1000
        long_result = self.scorer.score(long_text)
        self.assertIsInstance(long_result['risk_score'], float)
        
        # Special characters
        special_result = self.scorer.score("@#$%^&*()!")
        self.assertIsInstance(special_result['risk_score'], float)


if __name__ == '__main__':
    unittest.main()