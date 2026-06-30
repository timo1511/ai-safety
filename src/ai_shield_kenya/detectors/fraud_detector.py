import re
from typing import Dict, Any


class FraudDetector:
    """
    Detects financial scams and fake agricultural product claims.
    
    Kenyan context features:
    - Mobile money scams
    - Fake fertilizer products
    - Agricultural product fraud
    """
    
    def __init__(self):
        # Mobile money scam patterns
        self.mpesa_patterns = [
            r'\b(mpesa|mpesa|mobile money|send money|transfer|deposit|withdraw|bank account|account number|card number|cvv|pin|password)\b',
            r'\b(verify|confirm|activate|unlock|claim|prize|reward|bonus|gift|win|winner)\b.*\b(mpesa|money|cash|account|balance)\b',
            r'\b(send|pay|transfer)\s+\d+\s+(shilling|kes|ksh)\s+to\s+\d{10}\b'
        ]
        
        # Agricultural fraud patterns
        self.agriculture_patterns = [
            r'\b(fertilizer|pesticide|crop|seed|agriculture|farm|farmer)\b.*\b(fake|counterfeit|scam|fraud|fake|bogus|imitation)\b',
            r'\b(organic|natural|premium|high quality)\b.*\b(fertilizer|pesticide|seed)\b.*\b(cheap|discount|sale|offer)\b',
            r'\b(guarantee|100% effective|miracle|instant results|no side effects)\b.*\b(fertilizer|pesticide|seed)\b'
        ]
        
        # General fraud patterns
        self.general_patterns = [
            r'\b(scam|fraud|phishing|fake|counterfeit|deceive|cheat|rip off|con|swindle)\b',
            r'\b(urgent|immediate|limited time|act now|last chance|final warning)\b.*\b(action|response|payment|transfer)\b',
            r'\b(personal information|id number|national id|passport|address|phone number|email)\b.*\b(required|needed|must provide|submit)\b'
        ]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect fraud patterns in text.
        
        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()
        
        # Count matches for each pattern category
        mpesa_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.mpesa_patterns)
        agriculture_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.agriculture_patterns)
        general_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.general_patterns)
        
        # Calculate confidence score
        total_matches = mpesa_matches + agriculture_matches + general_matches
        confidence = min(1.0, total_matches * 0.2)  # Scale to 0-1
        
        # Determine severity
        if total_matches >= 3:
            severity = 'high'
        elif total_matches >= 2:
            severity = 'medium'
        elif total_matches >= 1:
            severity = 'low'
        else:
            severity = 'none'
        
        return {
            'is_fraud': total_matches > 0,
            'severity': severity,
            'confidence': round(confidence, 2),
            'mpesa_matches': mpesa_matches,
            'agriculture_matches': agriculture_matches,
            'general_matches': general_matches,
            'matched_patterns': [],
            'explanation': self._get_explanation(severity, mpesa_matches, agriculture_matches, general_matches)
        }
    
    def _get_explanation(self, severity: str, mpesa: int, agriculture: int, general: int) -> str:
        """Generate explanation based on detected patterns."""
        explanations = []
        
        if mpesa > 0:
            explanations.append("Mobile money scam indicators detected")
        if agriculture > 0:
            explanations.append("Agricultural product fraud indicators detected")
        if general > 0:
            explanations.append("General fraud indicators detected")
        
        if not explanations:
            return "No fraud patterns detected"
        
        return "; ".join(explanations) + f". Overall severity: {severity}."
import re
from typing import Dict, Any, List
from ..sir_model import SIRHarmModel


class FraudDetector:
    """
    Detects financial scams and fake agricultural product claims.
    """
    
    def __init__(self):
        # Kenyan-specific fraud patterns
        self.fraud_patterns = [
            r'\b(?:mpesa|mobile money|pesa ya simu)\b',
            r'\b(?:send|transfer|pay|deposit)\b.*?\b(?:money|cash|funds)\b',
            r'\b(?:urgent|immediate|now)\b.*?\b(?:payment|transfer|money)\b',
            r'\b(?:lottery|win|prize|jackpot)\b.*?\b(?:claim|receive|get)\b',
            r'\b(?:fake|counterfeit|imitation|fraudulent)\b.*?\b(?:product|fertilizer|pesticide|seed)\b',
            r'\b(?:guarantee|promise|assure)\b.*?\b(?:500%|100%|double|triple)\b.*?\b(?:yield|production|harvest)\b'
        ]
        
        # Swahili fraud patterns
        self.swahili_fraud_patterns = [
            r'\b(?:mpesa|pesa ya simu)\b',
            r'\b(?:kutuma|kufungua|kulipa)\b.*?\b(?:pesa|fedha)\b',
            r'\b(?:haraka|harakati|sasa)\b.*?\b(?:malipo|pesa)\b',
            r'\b(?:loteri|shinda|tuzo|jumbe)\b.*?\b(?:pata|pata kwa|pata sasa)\b',
            r'\b(?:uongo|uongo wa|uongo wa pesa)\b',
            r'\b(?:uhakika|ahadi|kubali)\b.*?\b(?:asalimia 500|asalimia 100|maradufu|kutoka mara mbili)\b'
        ]
        
        self.sir_model = SIRHarmModel()
        # Pre-fitted parameters for fraud detection
        self.sir_model.beta = 0.85
        self.sir_model.gamma = 0.15
        self.sir_model.fitted = True
    
    def detect(self, text: str, language: str = "en") -> Dict[str, Any]:
        """
        Detect fraud in the given text.
        
        Args:
            text: Input text to analyze
            language: Language code ('en', 'sw')
        
        Returns:
            Dictionary with detection results
        """
        # Check for fraud patterns
        pattern_matches = []
        patterns_to_check = self.fraud_patterns if language == "en" else self.swahili_fraud_patterns
        
        for i, pattern in enumerate(patterns_to_check):
            matches = re.findall(pattern, text.lower())
            if matches:
                pattern_matches.append({
                    "pattern_id": i,
                    "pattern": pattern,
                    "matches": matches,
                    "count": len(matches)
                })
        
        # Calculate risk score using SIR model
        context_complexity = 120 if language == "sw" else 100
        risk_score = self.sir_model.score_risk(text, context_complexity)
        
        # Determine severity
        if len(pattern_matches) >= 3:
            severity = "high"
        elif len(pattern_matches) >= 2:
            severity = "medium"
        elif len(pattern_matches) >= 1:
            severity = "low"
        else:
            severity = "none"
        
        return {
            "detected": len(pattern_matches) > 0,
            "severity": severity,
            "risk_score": round(risk_score, 1),
            "pattern_matches": pattern_matches,
            "explanation": self._generate_explanation(pattern_matches, severity),
            "recommendations": self._generate_recommendations(severity)
        }
    
    def _generate_explanation(self, pattern_matches: List[Dict[str, Any]], severity: str) -> str:
        """
        Generate explanation for fraud detection.
        """
        if not pattern_matches:
            return "No fraud patterns detected in the text."
        
        if severity == "high":
            return f"High-risk fraud detected with {len(pattern_matches)} matching patterns. This appears to be a sophisticated scam attempt."
        elif severity == "medium":
            return f"Medium-risk fraud detected with {len(pattern_matches)} matching patterns. Exercise caution before proceeding."
        else:
            return f"Low-risk fraud indicator detected with {len(pattern_matches)} matching pattern. Verify details carefully."
    
    def _generate_recommendations(self, severity: str) -> List[str]:
        """
        Generate recommendations based on fraud severity.
        """
        if severity == "high":
            return [
                "Do not send any money or personal information",
                "Report this to your mobile network provider immediately",
                "Contact Kenya Bankers Association for verification",
                "Consult with local agricultural extension officers"
            ]
        elif severity == "medium":
            return [
                "Verify the sender's identity through official channels",
                "Check for red flags like urgent requests or promises of high returns",
                "Consult with trusted community members before acting"
            ]
        else:
            return [
                "Be cautious about sharing personal or financial information",
                "Verify claims with official sources before taking action"
            ]

# Convenience function
def create_fraud_detector() -> FraudDetector:
    """
    Create and return a new FraudDetector instance.
    
    Returns:
        FraudDetector instance
    """
    return FraudDetector()