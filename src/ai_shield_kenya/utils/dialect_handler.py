from typing import Dict, Any


def handle_kisii_dialect(text: str) -> Dict[str, Any]:
    """
    Handle Kisii dialect text processing and translation.
    
    Returns:
        Dictionary with processed text and metadata
    """
    # Kisii dialect to English mapping (simplified)
    kisii_to_english = {
        'rie': 'I',
        'kie': 'you',
        'nyi': 'we',
        'nde': 'this',
        'riri': 'that',
        'kende': 'where',
        'chamuka': 'farm',
        'chabururu': 'school',
        'omokuria': 'farmer',
        'omogusii': 'teacher',
        'omosaba': 'student'
    }
    
    # Simple Kisii dialect detection and processing
    text_lower = text.lower()
    
    # Detect Kisii words
    kisii_words = []
    for kisii_word in kisii_to_english.keys():
        if kisii_word in text_lower:
            kisii_words.append(kisii_word)
    
    # Basic translation
    translated_text = text
    for kisii_word, english_word in kisii_to_english.items():
        translated_text = translated_text.replace(kisii_word, english_word)
        translated_text = translated_text.replace(kisii_word.capitalize(), english_word.capitalize())
    
    return {
        'original_text': text,
        'translated_text': translated_text,
        'kisii_words_detected': kisii_words,
        'translation_confidence': min(1.0, len(kisii_words) * 0.2),
        'is_kisii_dialect': len(kisii_words) > 0
    }
import re
from typing import Dict, Any, List


class KisiiDialectHandler:
    """
    Handle Kisii dialect variations and translations.
    """
    
    def __init__(self):
        # Kisii to English mapping (simplified)
        self.kisii_to_english = {
            "rie": "this",
            "kie": "that",
            "nyi": "you",
            "nde": "here",
            "riri": "there",
            "kende": "with",
            "chira": "disease",
            "machira": "disease",
            "mwa": "of",
            "kwa": "for",
            "na": "and"
        }
        
        # English to Kisii mapping
        self.english_to_kisii = {
            "this": "rie",
            "that": "kie",
            "you": "nyi",
            "here": "nde",
            "there": "riri",
            "with": "kende",
            "disease": "chira",
            "of": "mwa",
            "for": "kwa",
            "and": "na"
        }
        
        # Common Kisii patterns for harm detection
        self.harm_patterns = {
            "toxicity": [
                r'\b(?:chira|machira)\b.*?\b(?:sumu|baya|kufa)\b',
                r'\b(?:sumu|baya|kufa)\b.*?\b(?:chira|machira)\b'
            ],
            "fraud": [
                r'\b(?:rie|kie)\b.*?\b(?:uongo|uongo wa)\b',
                r'\b(?:uongo|uongo wa)\b.*?\b(?:rie|kie)\b'
            ],
            "misinformation": [
                r'\b(?:chira|machira)\b.*?\b(?:si sahihi|si kweli|uongo)\b',
                r'\b(?:si sahihi|si kweli|uongo)\b.*?\b(?:chira|machira)\b'
            ]
        }
    
    def translate_kisii_to_english(self, text: str) -> str:
        """
        Translate Kisii dialect to English.
        
        Args:
            text: Kisii text to translate
        
        Returns:
            Translated English text
        """
        words = text.split()
        translated = []
        
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[.,;:!?]+$', '', word)
            
            # Look up in dictionary
            if clean_word.lower() in self.kisii_to_english:
                translated.append(self.kisii_to_english[clean_word.lower()])
            else:
                translated.append(word)  # Keep original if not found
        
        return ' '.join(translated)
    
    def translate_english_to_kisii(self, text: str) -> str:
        """
        Translate English to Kisii dialect.
        
        Args:
            text: English text to translate
        
        Returns:
            Translated Kisii text
        """
        words = text.split()
        translated = []
        
        for word in words:
            # Remove punctuation
            clean_word = re.sub(r'[.,;:!?]+$', '', word)
            
            # Look up in dictionary
            if clean_word.lower() in self.english_to_kisii:
                translated.append(self.english_to_kisii[clean_word.lower()])
            else:
                translated.append(word)  # Keep original if not found
        
        return ' '.join(translated)
    
    def detect_harm_in_kisii(self, text: str, harm_type: str = "all") -> Dict[str, Any]:
        """
        Detect harm patterns in Kisii dialect text.
        
        Args:
            text: Kisii text to analyze
            harm_type: Type of harm to detect ('toxicity', 'fraud', 'misinformation', 'all')
        
        Returns:
            Dictionary with detection results
        """
        results = {
            "detected": False,
            "patterns": [],
            "harm_type": harm_type
        }
        
        if harm_type == "all":
            types_to_check = ["toxicity", "fraud", "misinformation"]
        else:
            types_to_check = [harm_type]
        
        for harm in types_to_check:
            if harm in self.harm_patterns:
                for pattern in self.harm_patterns[harm]:
                    matches = re.findall(pattern, text.lower())
                    if matches:
                        results["detected"] = True
                        results["patterns"].append({
                            "type": harm,
                            "pattern": pattern,
                            "matches": matches
                        })
        
        return results
    
    def get_kisii_confidence(self, text: str) -> float:
        """
        Calculate confidence that text is Kisii dialect.
        
        Args:
            text: Text to analyze
        
        Returns:
            Confidence score (0.0-1.0)
        """
        text_lower = text.lower()
        
        # Count Kisii keywords
        kisii_keywords = ['rie', 'kie', 'nyi', 'nde', 'riri', 'kende', 'chira', 'machira']
        kisii_count = sum(1 for kw in kisii_keywords if kw in text_lower)
        
        # Simple confidence calculation
        confidence = min(1.0, kisii_count * 0.2)
        
        return round(confidence, 2)

# Convenience function
def create_kisii_dialect_handler() -> KisiiDialectHandler:
    """
    Create and return a new KisiiDialectHandler instance.
    
    Returns:
        KisiiDialectHandler instance
    """
    return KisiiDialectHandler()