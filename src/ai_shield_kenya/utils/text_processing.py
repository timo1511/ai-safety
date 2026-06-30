import re
import string
from typing import Tuple, Optional


def preprocess_text(text: str, language: str = 'en') -> str:
    """
    Preprocess text for analysis.
    
    Args:
        text: Input text
        language: Language code ('en', 'sw', 'ki')
    
    Returns:
        Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Remove punctuation (except apostrophes for contractions)
    if language == 'en':
        # Keep apostrophes in English contractions
        text = re.sub(r'[^w\'\s]', ' ', text)
    else:
        # Remove all punctuation for other languages
        text = re.sub(r'[^w\s]', ' ', text)
    
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect language of text with confidence score.
    
    Returns:
        Tuple of (language_code, confidence_score)
    """
    text_lower = text.lower()
    
    # Swahili detection
    swahili_keywords = ['mimi', 'wewe', 'yeye', 'sisi', 'nyinyi', 'wao', 'ni', 'sio', 'hakuna', 'hakuna matata']
    sw_count = sum(1 for kw in swahili_keywords if kw in text_lower)
    
    # Kisii detection
    kisii_keywords = ['kisii', 'gusii', 'omokuria', 'omogusii', 'omosaba', 'chamuka', 'chabururu']
    ki_count = sum(1 for kw in kisii_keywords if kw in text_lower)
    
    # English is default
    en_count = len(re.findall(r'\b(the|and|or|but|in|on|at|to|for|of|with|by)\b', text_lower))
    
    # Calculate confidence scores
    total_keywords = sw_count + ki_count + en_count
    
    if total_keywords == 0:
        return 'en', 0.5
    
    sw_confidence = sw_count / total_keywords
    ki_confidence = ki_count / total_keywords
    en_confidence = en_count / total_keywords
    
    # Determine best match
    if sw_confidence > ki_confidence and sw_confidence > en_confidence:
        return 'sw', round(sw_confidence, 2)
    elif ki_confidence > sw_confidence and ki_confidence > en_confidence:
        return 'ki', round(ki_confidence, 2)
    else:
        return 'en', round(en_confidence, 2)
import re
import string
from typing import Dict, Any


def preprocess_text(text: str, language: str = "en") -> str:
    """
    Preprocess text for harm detection.
    
    Args:
        text: Input text to preprocess
        language: Language code ('en', 'sw', 'ki')
    
    Returns:
        Preprocessed text
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Handle language-specific preprocessing
    if language == "sw":
        # Swahili-specific cleaning
        text = _clean_swahili(text)
    elif language == "ki":
        # Kisii dialect cleaning
        text = _clean_kisii(text)
    
    return text


def _clean_swahili(text: str) -> str:
    """
    Clean Swahili text.
    """
    # Remove common Swahili punctuation variations
    text = re.sub(r'[.,;:!?]+', ' ', text)
    
    # Normalize common Swahili contractions
    text = re.sub(r'\bni\b', 'ni', text)
    text = re.sub(r'\bna\b', 'na', text)
    text = re.sub(r'\bwa\b', 'wa', text)
    
    return text


def _clean_kisii(text: str) -> str:
    """
    Clean Kisii dialect text.
    """
    # Remove common Kisii punctuation variations
    text = re.sub(r'[.,;:!?]+', ' ', text)
    
    # Normalize common Kisii words
    text = re.sub(r'\brie\b', 'rie', text)
    text = re.sub(r'\bkie\b', 'kie', text)
    text = re.sub(r'\bnyi\b', 'nyi', text)
    
    return text


def detect_language(text: str) -> Dict[str, Any]:
    """
    Detect language of text using simple heuristics.
    
    Args:
        text: Input text to analyze
    
    Returns:
        Dictionary with detected language and confidence
    """
    text_lower = text.lower()
    
    # Count Swahili keywords
    swahili_keywords = ['mimi', 'wewe', 'yeye', 'sisi', 'ninyi', 'wao', 'ni', 'ndiyo', 'hapana', 'kwa', 'ya', 'wa']
    swahili_count = sum(1 for kw in swahili_keywords if kw in text_lower)
    
    # Count Kisii keywords (simplified)
    kisii_keywords = ['rie', 'kie', 'nyi', 'nde', 'riri', 'kende']
    kisii_count = sum(1 for kw in kisii_keywords if kw in text_lower)
    
    # English is default
    confidence = 0.5
    detected_lang = "en"
    
    if swahili_count > kisii_count and swahili_count >= 2:
        detected_lang = "sw"
        confidence = min(0.95, 0.5 + swahili_count * 0.1)
    elif kisii_count > swahili_count and kisii_count >= 2:
        detected_lang = "ki"
        confidence = min(0.90, 0.5 + kisii_count * 0.1)
    
    return {
        "language": detected_lang,
        "confidence": round(confidence, 2),
        "swahili_score": swahili_count,
        "kisii_score": kisii_count
    }

# Convenience functions
def clean_text(text: str, language: str = "en") -> str:
    """
    Alias for preprocess_text.
    """
    return preprocess_text(text, language)


def get_language_confidence(text: str) -> float:
    """
    Get confidence score for language detection.
    """
    result = detect_language(text)
    return result["confidence"]