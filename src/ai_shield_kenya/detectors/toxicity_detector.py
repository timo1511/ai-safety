import re
from typing import Dict, Any


class ToxicityDetector:
    """
    Detects harmful chemical advice, dangerous traditional medicine claims, and cultural toxicity.
    
    Features:
    - Swahili toxicity lexicon + English toxicity patterns
    - Cultural context awareness (respectful disagreement vs. toxicity)
    """
    
    def __init__(self):
        # Toxicity patterns
        self.toxicity_patterns = [
            r'\b(bleach|chemical|poison|toxic|dangerous|deadly|harmful|kill|destroy|fatal|lethal|corrosive|caustic)\b.*\b(plant|crop|soil|human|person|child|animal|livestock)\b',
            r'\b(traditional medicine|herbal remedy|natural cure|home remedy)\b.*\b(dangerous|toxic|kill|harm|deadly|fatal|unsafe)\b',
            r'\b(abuse|harass|bully|threat|attack|violence|discriminate|oppress|persecute|intimidate|coerce)\b',
            r'\b(hate|racist|sexist|homophobic|transphobic|bigot|prejudice|discrimination|bias)\b',
            r'\b(suicide|self harm|cut|burn|overdose|end life|give up|die)\b'
        ]
        
        # Swahili toxicity patterns
        self.swahili_toxicity_patterns = [
            r'\b(moto|sumu|hatari|kufa|kuua|kuharibu|kuchoma|kupiga|kushikilia|kudhoofisha)\b.*\b(mzao|mboga|shamba|mtu|mtoto|mdogo|mvulana|msichana)\b',
            r'\b(dawa ya kienyeji|dawa ya asili|mchakato wa nyumbani)\b.*\b(hatari|sumu|kufa|kuua|kupoteza maisha)\b',
            r'\b(kushutumu|kuchukua|kushikilia|kudhoofisha|kupigania|kudhoofisha|kushikilia)\b',
            r'\b(ubaya|ubovu|ubavu|ubovu wa rangi|ubovu wa jinsia|ubovu wa kijinsia|ubovu wa kipembe)\b'
        ]
        
        # Contextual patterns (to distinguish respectful disagreement from toxicity)
        self.contextual_patterns = [
            r'\b(respectfully|with respect|I disagree|however|but|although|while|on the other hand)\b',
            r'\b(evidence suggests|research shows|studies indicate|data indicates)\b',
            r'\b(constructive criticism|feedback|suggestion|recommendation|improvement)\b'
        ]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect toxicity patterns in text.
        
        Returns:
            Dictionary with detection results
        """
        text_lower = text.lower()
        
        # Count matches for each pattern category
        toxicity_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.toxicity_patterns)
        swahili_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.swahili_toxicity_patterns)
        contextual_matches = sum(len(re.findall(pattern, text_lower)) for pattern in self.contextual_patterns)
        
        # Calculate confidence score
        # Higher confidence if toxicity patterns match without contextual mitigators
        base_confidence = min(1.0, (toxicity_matches + swahili_matches) * 0.3)
        
        # Reduce confidence if contextual patterns are present (indicating respectful discourse)
        if contextual_matches > 0:
            base_confidence *= 0.5
        
        confidence = round(base_confidence, 2)
        
        # Determine severity
        if toxicity_matches + swahili_matches >= 3:
            severity = 'high'
        elif toxicity_matches + swahili_matches >= 2:
            severity = 'medium'
        elif toxicity_matches + swahili_matches >= 1:
            severity = 'low'
        else:
            severity = 'none'
        
        return {
            'is_toxic': (toxicity_matches + swahili_matches) > 0,
            'severity': severity,
            'confidence': confidence,
            'toxicity_matches': toxicity_matches,
            'swahili_matches': swahili_matches,
            'contextual_matches': contextual_matches,
            'matched_patterns': [],
            'explanation': self._get_explanation(severity, toxicity_matches, swahili_matches, contextual_matches)
        }
    
    def _get_explanation(self, severity: str, toxicity: int, swahili: int, contextual: int) -> str:
        """Generate explanation based on detected patterns."""
        explanations = []
        
        if toxicity > 0:
            explanations.append("English toxicity indicators detected")
        if swahili > 0:
            explanations.append("Swahili toxicity indicators detected")
        if contextual > 0:
            explanations.append("Contextual mitigators detected (may reduce toxicity severity)")
        
        if not explanations:
            return "No toxicity patterns detected"
        
        return "; ".join(explanations) + f". Overall severity: {severity}."
