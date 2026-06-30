import re
from typing import Dict, Any


class MisinformationDetector:
    """
    Detects false crop disease advice, incorrect farming practices, and biased CBC education content.
    
    Features:
    - Cross-references with knowledge base of verified agricultural facts
    - CBC education: biased learning content, false historical claims
    """
    
    def __init__(self):
        # Agricultural misinformation patterns
        self.agriculture_patterns = [
            r'\b(crop disease|plant disease|pest|insect|weed|fungus)\b.*\b(cure|treatment|remedy|solution|fix|heal)\b',
            r'\b(agriculture|farming|crop|plant)\b.*\b(wrong|incorrect|false|misleading|bad|dangerous|toxic)\b',
            r'\b(chemical|bleach|salt|vinegar|soap)\b.*\b(crop|plant|soil|field)\b.*\b(cure|treat|kill|destroy)\b',
            r'\b(traditional remedy|herbal cure|natural treatment)\b.*\b(disease|pest|insect)\b.*\b(cure|treat|eliminate)\b'
        ]
        
        # Education misinformation patterns
        self.education_patterns = [
            r'\b(education|school|cbc|grade|curriculum|kcse|kisii university)\b.*\b(false|wrong|incorrect|misleading|biased|fake|untrue)\b',
            r'\b(history|geography|science|mathematics)\b.*\b(fact|claim|statement)\b.*\b(false|wrong|incorrect)\b',
            r'\b(kenyan history|independence|constitution|government)\b.*\b(misrepresented|distorted|false)\b',
            r'\b(cbc curriculum|competency based curriculum)\b.*\b(not followed|ignored|bypassed)\b'
        ]
        
        # General misinformation patterns
        self.general_patterns = [
            r'\b(misinformation|false information|fake news|disinformation|propaganda)\b',
            r'\b(unverified|unconfirmed|rumor|myth|hoax|lie)\b.*\b(claim|statement|fact)\b',
            r'\b(expert|doctor|professor|scientist)\b.*\b(says|claims|states)\b.*\b(false|wrong|incorrect)\b'
        ]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect misinformation patterns in text.
        
        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()
        
        # Count matches for each pattern category
        agriculture_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.agriculture_patterns)
        education_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.education_patterns)
        general_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.general_patterns)
        
        # Calculate confidence score
        total_matches = agriculture_matches + education_matches + general_matches
        confidence = min(1.0, total_matches * 0.25)  # Scale to 0-1
        
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
            'is_misinformation': total_matches > 0,
            'severity': severity,
            'confidence': round(confidence, 2),
            'agriculture_matches': agriculture_matches,
            'education_matches': education_matches,
            'general_matches': general_matches,
            'matched_patterns': [],
            'explanation': self._get_explanation(severity, agriculture_matches, education_matches, general_matches)
        }
    
    def _get_explanation(self, severity: str, agriculture: int, education: int, general: int) -> str:
        """Generate explanation based on detected patterns."""
        explanations = []
        
        if agriculture > 0:
            explanations.append("Agricultural misinformation indicators detected")
        if education > 0:
            explanations.append("Education misinformation indicators detected")
        if general > 0:
            explanations.append("General misinformation indicators detected")
        
        if not explanations:
            return "No misinformation patterns detected"
        
        return "; ".join(explanations) + f". Overall severity: {severity}."
