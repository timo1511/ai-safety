#!/usr/bin/env python3
"""
AI Shield Kenya Text Processing Test

Test the text processing and dialect handling functionality.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.utils.text_processing import preprocess_text, detect_language
    from ai_shield_kenya.utils.dialect_handler import KisiiDialectHandler
    
    print("✅ Text processing imports successful!")
    
    # Test preprocess_text
    original = "Use BLEACH to cure crop disease!"
    processed = preprocess_text(original, language="en")
    if processed == "use bleach to cure crop disease":
        print("✅ English preprocessing works")
    else:
        print(f"❌ English preprocessing failed: expected 'use bleach to cure crop disease', got '{processed}'")
        sys.exit(1)
    
    # Test Swahili preprocessing
    sw_original = "Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach!"
    sw_processed = preprocess_text(sw_original, language="sw")
    if "ugonjwa" in sw_processed and "bleach" in sw_processed:
        print("✅ Swahili preprocessing works")
    else:
        print("❌ Swahili preprocessing failed")
        sys.exit(1)
    
    # Test language detection
    lang_result = detect_language("Ugonjwa wa MLN ni ugonjwa muhimu wa virusi")
    if lang_result["language"] == "sw" and lang_result["confidence"] > 0.8:
        print(f"✅ Swahili detection works: {lang_result['language']} (confidence {lang_result['confidence']:.2f})")
    else:
        print("❌ Swahili detection failed")
        sys.exit(1)
    
    # Test English detection
    en_result = detect_language("This is an English sentence")
    if en_result["language"] == "en":
        print(f"✅ English detection works: {en_result['language']} (confidence {en_result['confidence']:.2f})")
    else:
        print("❌ English detection failed")
        sys.exit(1)
    
    # Test Kisii dialect handler
    kd_handler = KisiiDialectHandler()
    
    # Test Kisii translation
    kisii_text = "rie chira ni rieto"
    english_translation = kd_handler.translate_kisii_to_english(kisii_text)
    if "this disease" in english_translation.lower():
        print("✅ Kisii to English translation works")
    else:
        print("❌ Kisii translation failed")
        sys.exit(1)
    
    # Test Kisii confidence
    kisii_confidence = kd_handler.get_kisii_confidence(kisii_text)
    if kisii_confidence > 0.5:
        print(f"✅ Kisii confidence calculation works: {kisii_confidence:.2f}")
    else:
        print("❌ Kisii confidence calculation failed")
        sys.exit(1)
    
    print("\n🎉 All text processing tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)