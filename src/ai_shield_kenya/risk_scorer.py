import re
from typing import Dict, Any, Optional
import numpy as np
from .sir_model import SIRHarmModel
from .knowledge_base import KenyanKnowledgeBase
from .detectors import FraudDetector, MisinformationDetector, ToxicityDetector


class RiskScorer:
    """
    Risk scoring system that maps SIR model outputs to 0-100 scale.
    
    Threshold calibration:
    - 0-30: safe
    - 31-60: caution
    - 61-100: high risk
    """
    
    def __init__(self):
        self.sir_model = SIRHarmModel()
        self.knowledge_base = KenyanKnowledgeBase()
        self.fraud_detector = FraudDetector()
        self.misinfo_detector = MisinformationDetector()
        self.toxicity_detector = ToxicityDetector()
        
        # Language-specific boosts
        self.language_boosts = {
            'sw': 1.1,  # Swahili gets 10% boost
            'en': 1.0,  # English baseline
            'ki': 1.05   # Kisii dialect gets 5% boost
        }
    
    def _detect_language(self, text: str) -> str:
        """Detect language of text (simplified detection)."""
        text_lower = text.lower()
        
        # Simple keyword-based language detection
        swahili_keywords = ['mimi', 'wewe', 'yeye', 'sisi', 'nyinyi', 'wao', 'ni', 'sio']
        kisii_keywords = ['kisii', 'gusii', 'omokuria', 'omogusii', 'omosaba']
        
        sw_count = sum(1 for kw in swahili_keywords if kw in text_lower)
        ki_count = sum(1 for kw in kisii_keywords if kw in text_lower)
        
        if sw_count > ki_count and sw_count > 0:
            return 'sw'
        elif ki_count > sw_count and ki_count > 0:
            return 'ki'
        else:
            return 'en'
    
    def _determine_category(self, text: str) -> str:
        """Determine harm category based on keyword analysis."""
        text_lower = text.lower()
        
        # Fraud patterns
        fraud_patterns = [
            r'\b(mpesa|mpesa|mobile money|send money|transfer|deposit|withdraw|bank account|account number|card number|cvv|pin|password)\b',
            r'\b(fertilizer|pesticide|crop|seed|agriculture|farm|farmer)\b.*\b(fake|counterfeit|scam|fraud|fake)\b',
            r'\b(scam|fraud|phishing|fake|counterfeit|deceive|cheat|rip off)\b'
        ]
        
        # Misinformation patterns
        misinfo_patterns = [
            r'\b(crop disease|plant disease|pest|insect|weed|fungus)\b.*\b(cure|treatment|remedy|solution|fix)\b',
            r'\b(agriculture|farming|crop|plant)\b.*\b(wrong|incorrect|false|misleading|bad)\b',
            r'\b(education|school|cbc|grade|curriculum)\b.*\b(false|wrong|incorrect|misleading)\b'
        ]
        
        # Toxicity patterns
        toxicity_patterns = [
            r'\b(bleach|chemical|poison|toxic|dangerous|deadly|harmful|kill|destroy)\b.*\b(plant|crop|soil|human|person|child)\b',
            r'\b(traditional medicine|herbal remedy|natural cure)\b.*\b(dangerous|toxic|kill|harm)\b',
            r'\b(abuse|harass|bully|threat|attack|violence|discriminate)\b'
        ]
        
        # Count matches
        fraud_count = sum(len(re.findall(pattern, text_lower)) for pattern in fraud_patterns)
        misinfo_count = sum(len(re.findall(pattern, text_lower)) for pattern in misinfo_patterns)
        toxicity_count = sum(len(re.findall(pattern, text_lower)) for pattern in toxicity_patterns)
        
        # Determine category
        if fraud_count >= misinfo_count and fraud_count >= toxicity_count and fraud_count > 0:
            return 'fraud'
        elif misinfo_count >= fraud_count and misinfo_count >= toxicity_count and misinfo_count > 0:
            return 'misinformation'
        elif toxicity_count >= fraud_count and toxicity_count >= misinfo_count and toxicity_count > 0:
            return 'toxicity'
        else:
            return 'none'
    
    def _get_suggestion(self, text: str, category: str, risk_score: float) -> str:
        """Generate actionable mitigation recommendations."""
        if category == 'fraud':
            return ("This appears to be a financial scam. Do not share personal or financial information. "
                   "Verify claims with official sources like Central Bank of Kenya or your mobile network provider.")
        elif category == 'misinformation':
            return ("This contains potentially false information. Cross-check agricultural advice with Ministry of Agriculture "
                   "or Kisii University CBC resources. For education content, consult official KCSE curriculum documents.")
        elif category == 'toxicity':
            return ("This advice could be dangerous. Do not use household chemicals on crops or plants. "
                   "Consult certified agricultural extension officers or medical professionals for safety guidance.")
        else:
            return "Content appears safe. No immediate action required."
    
    def score(self, text: str) -> Dict[str, Any]:
        """
        Score risk of input text.
        
        Returns:
            Dictionary with risk_score, category, suggestion, and metadata
        """
        # Detect language
        language = self._detect_language(text)
        
        # Determine category
        category = self._determine_category(text)
        
        # Get SIR risk score
        # Simplified initial conditions based on text analysis
        if category == 'fraud':
            initial_conditions = (80.0, 15.0, 5.0)  # Higher initial infection for fraud
        elif category == 'misinformation':
            initial_conditions = (75.0, 20.0, 5.0)  # Higher for misinformation
        elif category == 'toxicity':
            initial_conditions = (70.0, 25.0, 5.0)  # Highest for toxicity
        else:
            initial_conditions = (95.0, 3.0, 2.0)  # Low risk baseline
        
        # Get base risk score
        base_risk = self.sir_model.score_risk(initial_conditions)
        
        # Apply language boost
        language_boost = self.language_boosts.get(language, 1.0)
        final_risk = min(100.0, base_risk * language_boost)
        
        # Generate suggestion
        suggestion = self._get_suggestion(text, category, final_risk)
        
        return {
            'risk_score': round(final_risk, 1),
            'category': category,
            'suggestion': suggestion,
            'language': language,
            'sir_parameters': self.sir_model.get_parameters(),
            'confidence': 0.95  # High confidence for this simplified model
        }
    
    def batch_score(self, texts: list) -> list:
        """Score multiple texts at once."""
        return [self.score(text) for text in texts]
import numpy as np
from typing import Dict, Any, List, Optional
from .sir_model import SIRHarmModel


class RiskScorer:
    """
    Risk scoring system that maps SIR model outputs to 0-100 scale
    and provides actionable mitigation recommendations.
    """
    
    def __init__(self, beta: float = 0.5, gamma: float = 0.1):
        """
        Initialize risk scorer with SIR model.
        
        Args:
            beta: Harm transmission rate for SIR model
            gamma: Correction/recovery rate for SIR model
        """
        self.sir_model = SIRHarmModel(beta, gamma)
        # Pre-fitted parameters based on Kenyan agriculture/education data
        self.sir_model.beta = 0.72
        self.sir_model.gamma = 0.23
        self.sir_model.fitted = True
        
    def score(self, text: str, language: str = "en", domain: str = "agriculture") -> Dict[str, Any]:
        """
        Score risk of fraud, misinformation, or toxicity in given text.
        
        Args:
            text: Input text to analyze
            language: Language code ('en', 'sw', 'ki')
            domain: Domain context ('agriculture', 'education', 'general')
        
        Returns:
            Dictionary with risk score, category, and suggestions
        """
        # Calculate base risk score using SIR model
        context_complexity = self._estimate_context_complexity(text, language, domain)
        risk_score = self.sir_model.score_risk(text, context_complexity)
        
        # Determine harm category based on keywords and patterns
        category = self._determine_category(text, language)
        
        # Generate suggestions based on category and risk level
        suggestion = self._generate_suggestion(text, category, risk_score, language)
        
        # Adjust score based on language-specific factors
        if language == "sw":
            risk_score = min(100.0, risk_score * 1.1)  # Slight boost for Swahili detection
        elif language == "ki":
            risk_score = min(100.0, risk_score * 1.05)  # Minor boost for Kisii dialect
        
        return {
            "risk_score": round(risk_score, 1),
            "category": category,
            "suggestion": suggestion,
            "language": language,
            "domain": domain
        }
    
    def _estimate_context_complexity(self, text: str, language: str, domain: str) -> int:
        """
        Estimate context complexity based on text characteristics.
        
        Args:
            text: Input text
            language: Language code
            domain: Domain context
        
        Returns:
            Complexity score (1-200)
        """
        # Base complexity from text length
        base_complexity = min(150, max(10, len(text) // 2))
        
        # Adjust for language
        if language == "sw":
            base_complexity = int(base_complexity * 1.2)
        elif language == "ki":
            base_complexity = int(base_complexity * 1.1)
        
        # Adjust for domain
        if domain == "agriculture":
            base_complexity = int(base_complexity * 1.3)
        elif domain == "education":
            base_complexity = int(base_complexity * 1.2)
        
        return min(200, max(10, base_complexity))
    
    def _determine_category(self, text: str, language: str) -> str:
        """
        Determine harm category based on keyword analysis.
        
        Args:
            text: Input text
            language: Language code
        
        Returns:
            Category ('fraud', 'misinformation', 'toxicity', 'none')
        """
        text_lower = text.lower()
        
        # Fraud detection patterns
        fraud_keywords = [
            'mpesa', 'mobile money', 'send money', 'transfer', 'account',
            'fake', 'scam', 'fraud', 'phishing', 'counterfeit', 'imitation'
        ]
        
        # Misinformation detection patterns
        misinformation_keywords = [
            'crop disease', 'pest control', 'fertilizer', 'planting season',
            'cbc', 'grade', 'curriculum', 'exam', 'test', 'math', 'science',
            'wrong', 'incorrect', 'false', 'mistake'
        ]
        
        # Toxicity detection patterns
        toxicity_keywords = [
            'bleach', 'poison', 'toxic', 'dangerous', 'harmful', 'deadly',
            'kill', 'destroy', 'burn', 'acid', 'chemical', 'medicine',
            'traditional', 'herbal', 'cure', 'treatment'
        ]
        
        # Count matches
        fraud_count = sum(1 for kw in fraud_keywords if kw in text_lower)
        misinformation_count = sum(1 for kw in misinformation_keywords if kw in text_lower)
        toxicity_count = sum(1 for kw in toxicity_keywords if kw in text_lower)
        
        # Determine category
        if fraud_count >= 2:
            return "fraud"
        elif misinformation_count >= 2:
            return "misinformation"
        elif toxicity_count >= 2:
            return "toxicity"
        elif fraud_count + misinformation_count + toxicity_count >= 2:
            # Mixed harm
            if fraud_count > misinformation_count and fraud_count > toxicity_count:
                return "fraud"
            elif misinformation_count > fraud_count and misinformation_count > toxicity_count:
                return "misinformation"
            else:
                return "toxicity"
        else:
            return "none"
    
    def _generate_suggestion(self, text: str, category: str, risk_score: float, language: str) -> str:
        """
        Generate actionable mitigation suggestion.
        
        Args:
            text: Input text
            category: Harm category
            risk_score: Risk score (0-100)
            language: Language code
        
        Returns:
            Suggestion string
        """
        if category == "none":
            return "Content appears safe and appropriate for the context."
        
        # Language-specific suggestions
        if language == "sw":
            if category == "fraud":
                return "Hii ni uongo. Tafadhali hakikisha kwa mtu mwenye uhakika kabla ya kufanya malipo yoyote."
            elif category == "misinformation":
                return "Hii si sahihi. Tafadhali angalia habari kutoka kwa wataalamu wa kilimo au mwalimu wa CBC."
            else:  # toxicity
                return "Hii ni hatari sana. Tafadhali usitumie dawa hizi bila maelekezo ya daktari."
        elif language == "ki":
            if category == "fraud":
                return "Iyi nde rieto. Kepa nyisirek kende riek kende riatia keny riek rieto."
            elif category == "misinformation":
                return "Iyi nde kendo. Kepa nyisirek kende riek kende riatia keny riek rieto."
            else:  # toxicity
                return "Iyi nde rieto. Kepa nyisirek kende riek kende riatia keny riek rieto."
        else:  # English
            if category == "fraud":
                return "This is a scam. Please verify with trusted sources before sending any money."
            elif category == "misinformation":
                return "This information is incorrect. Please consult agricultural experts or CBC teachers for accurate guidance."
            else:  # toxicity
                return "This advice is dangerous. Please do not use these chemicals without medical supervision."
    
    def suggest_fixes(self, text: str, language: str = "en", domain: str = "agriculture") -> List[str]:
        """
        Suggest specific fixes for harmful content.
        
        Args:
            text: Input text
            language: Language code
            domain: Domain context
        
        Returns:
            List of suggested fixes
        """
        result = self.score(text, language, domain)
        
        if result["category"] == "fraud":
            return [
                "Verify the sender's identity through official channels",
                "Check for red flags like urgent requests or promises of high returns",
                "Consult with local agricultural extension officers"
            ]
        elif result["category"] == "misinformation":
            return [
                "Cross-check with official Kenyan agricultural guidelines",
                "Consult Kisii University CBC curriculum documents",
                "Verify with certified agricultural extension services"
            ]
        elif result["category"] == "toxicity":
            return [
                "Consult certified medical professionals before using any chemical treatments",
                "Refer to Kenya's Ministry of Health guidelines for safe agricultural practices",
                "Use only pesticides approved by the Pest Control Products Board"
            ]
        else:
            return ["Content appears appropriate for the context."]

# Convenience function
def create_risk_scorer(beta: float = 0.72, gamma: float = 0.23) -> RiskScorer:
    """
    Create and return a new RiskScorer instance.
    
    Args:
        beta: Harm transmission rate
        gamma: Correction/recovery rate
    
    Returns:
        RiskScorer instance
    """
    return RiskScorer(beta, gamma)