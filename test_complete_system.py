#!/usr/bin/env python3
"""
AI Shield Kenya Complete System Test

Test the entire AI Shield Kenya system end-to-end.
"""

import sys
import os
import numpy as np

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    # Import all main components
    from ai_shield_kenya import RiskScorer
    from ai_shield_kenya.sir_model import SIRHarmModel
    from ai_shield_kenya.knowledge_base import KenyanKnowledgeBase
    from ai_shield_kenya.detectors import FraudDetector, MisinformationDetector, ToxicityDetector
    from ai_shield_kenya.evaluators import F1Evaluator
    from ai_shield_kenya.utils.text_processing import detect_language
    
    print("✅ All core imports successful!")
    
    # Initialize components
    scorer = RiskScorer()
    model = SIRHarmModel()
    kb = KenyanKnowledgeBase()
    fraud_detector = FraudDetector()
    misinfo_detector = MisinformationDetector()
    toxicity_detector = ToxicityDetector()
    evaluator = F1Evaluator()
    
    print("✅ All components initialized!")
    
    # Test end-to-end scoring
    test_prompts = [
        "Use bleach to cure crop disease",
        "CBC Math Grade 4: 2+2=5",
        "Send KSh 5000 to M-Pesa number 0712345678",
        "Mafuta ya neem ni dawa ya wadudu ya kimwili ambayo inatumika kwa usalama kwenye mimea"
    ]
    
    results = []
    for prompt in test_prompts:
        result = scorer.score(prompt)
        results.append(result)
        
        if 'risk_score' not in result or not isinstance(result['risk_score'], (int, float)):
            print(f"❌ Score failed for '{prompt}'")
            sys.exit(1)
    
    print(f"✅ End-to-end scoring works for {len(results)} prompts")
    
    # Test language detection
    lang_result = detect_language("Ugonjwa wa MLN ni ugonjwa muhimu wa virusi")
    if lang_result["language"] == "sw":
        print(f"✅ Language detection works: {lang_result['language']} (confidence {lang_result['confidence']:.2f})")
    else:
        print("❌ Language detection failed")
        sys.exit(1)
    
    # Test knowledge base query
    facts = kb.query("maize disease", language="en")
    if len(facts) > 0:
        print(f"✅ Knowledge base query works: found {len(facts)} facts")
    else:
        print("❌ Knowledge base query failed")
        sys.exit(1)
    
    # Test detector integration
    fraud_result = fraud_detector.detect("Send money to unknown M-Pesa number")
    if fraud_result["detected"]:
        print(f"✅ Detector integration works: {fraud_result['severity']} risk detected")
    else:
        print("❌ Detector integration failed")
        sys.exit(1)
    
    print("\n🎉 AI Shield Kenya complete system verification passed!")
    print("All components work together successfully.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)