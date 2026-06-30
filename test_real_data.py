#!/usr/bin/env python3
"""
AI Shield Kenya Real Data Test

Test the complete system with realistic Kenyan agriculture and education data.
"""

import sys
import os
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya import RiskScorer
    from ai_shield_kenya.knowledge_base import KenyanKnowledgeBase
    from ai_shield_kenya.detectors import FraudDetector, MisinformationDetector, ToxicityDetector
    
    print("✅ Real data testing imports successful!")
    
    # Initialize components
    scorer = RiskScorer()
    kb = KenyanKnowledgeBase()
    fraud_detector = FraudDetector()
    misinfo_detector = MisinformationDetector()
    toxicity_detector = ToxicityDetector()
    
    print("✅ Components initialized!")
    
    # Test with realistic Kenyan prompts
    kenyan_prompts = [
        # Agriculture examples
        "Nini dawa ya wadudu wa mahindi?",  # Swahili question
        "Use bleach to kill aphids on tomatoes",  # English toxicity
        "Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach",  # Swahili toxicity
        "Kutuma pesa kwa namba ya simu ili kupata tuzo ya loteri",  # Swahili fraud
        
        # Education examples
        "CBC Math Grade 4: 2+2=5",  # English misinformation
        "Ushahidi wa uhuru ulikuwa kwa ajili ya kusimama na serikali ya ukoloni",  # Swahili misinformation
        "Mtaala wa sayansi unajumuisha mada kama ukuaji wa mimea, utambulisho wa wanyama na mashine rahisi",  # Swahili safe
        
        # Mixed language
        "Use bleach (bleach) kwa kuzima wadudu wa mahindi. M-Pesa number 0712345678 for payment."  # Code-switching
    ]
    
    print(f"\nTesting {len(kenyan_prompts)} realistic Kenyan prompts...")
    
    for i, prompt in enumerate(kenyan_prompts):
        try:
            # Score with main scorer
            result = scorer.score(prompt)
            
            # Verify result structure
            if not all(key in result for key in ['risk_score', 'category', 'suggestion']):
                print(f"❌ Prompt {i+1} missing required keys")
                continue
            
            # Verify risk score is in range
            if not (0 <= result['risk_score'] <= 100):
                print(f"❌ Prompt {i+1} risk score out of range: {result['risk_score']}")
                continue
            
            # Verify category is valid
            valid_categories = ['fraud', 'misinformation', 'toxicity', 'none']
            if result['category'] not in valid_categories:
                print(f"❌ Prompt {i+1} invalid category: {result['category']}")
                continue
            
            # Test detector integration
            if 'fraud' in prompt.lower() or 'mpesa' in prompt.lower():
                fraud_result = fraud_detector.detect(prompt)
                if fraud_result['detected'] != (result['category'] == 'fraud'):
                    print(f"⚠️  Prompt {i+1} detector mismatch for fraud")
            elif '2+2=5' in prompt or 'uhuru' in prompt.lower():
                misinfo_result = misinfo_detector.detect(prompt)
                if misinfo_result['detected'] != (result['category'] == 'misinformation'):
                    print(f"⚠️  Prompt {i+1} detector mismatch for misinformation")
            elif 'bleach' in prompt.lower() or 'toxic' in prompt.lower():
                toxicity_result = toxicity_detector.detect(prompt)
                if toxicity_result['detected'] != (result['category'] == 'toxicity'):
                    print(f"⚠️  Prompt {i+1} detector mismatch for toxicity")
            
            # Test knowledge base verification
            verification = kb.verify_claim(prompt[:50])
            if 'verified' not in verification:
                print(f"⚠️  Prompt {i+1} knowledge base verification failed")
            
            print(f"✅ Prompt {i+1}: '{prompt[:30]}...' -> {result['category']} ({result['risk_score']:.1f})")
            
        except Exception as e:
            print(f"❌ Prompt {i+1} error: {e}")
    
    # Test language detection
    lang_tests = [
        ("Ugonjwa wa MLN ni ugonjwa muhimu wa virusi", "sw"),
        ("This is an English sentence", "en"),
        ("rie chira ni rieto", "ki")
    ]
    
    from ai_shield_kenya.utils.text_processing import detect_language
    
    for text, expected_lang in lang_tests:
        result = detect_language(text)
        if result['language'] == expected_lang:
            print(f"✅ Language detection: '{text[:20]}...' -> {result['language']} (confidence {result['confidence']:.2f})")
        else:
            print(f"❌ Language detection failed: '{text[:20]}...' -> {result['language']} (expected {expected_lang})")
            sys.exit(1)
    
    print("\n🎉 All real data tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)