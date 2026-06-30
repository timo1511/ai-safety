from .text_processing import preprocess_text, detect_language
from .dialect_handler import handle_kisii_dialect

__all__ = [
    "preprocess_text",
    "detect_language",
    "handle_kisii_dialect"
]
from .text_processing import preprocess_text, detect_language
from .dialect_handler import KisiiDialectHandler

__all__ = [
    "preprocess_text",
    "detect_language",
    "KisiiDialectHandler"
]