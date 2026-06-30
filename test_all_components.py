#!/usr/bin/env python3
"""
AI Shield Kenya All Components Test

Test that all components work together in harmony.
"""

import sys
import os
import numpy as np
from pathlib import Path

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
    from ai_shield_kenya.utils.dialect_handler import KisiiDialectHandler
    
    print("✅ All component imports successful!")
    
    # Initialize all components
    scorer = RiskScorer()
    model = SIRHarmModel()
    kb = KenyanKnowledgeBase()
    fraud_detector = FraudDetector()
    misinfo_detector = MisinformationDetector()
    toxicity_detector = ToxicityDetector()
    evaluator = F1Evaluator()
    kd_handler = KisiiDialectHandler()
    
    print("✅ All components initialized!")
    
    # Test integration scenarios
    scenarios = [
        {
            "name": "Agriculture Fraud",
            "prompt": "Kutuma pesa kwa namba ya simu ili kupata tuzo ya loteri",
            "language": "sw",
            "domain": "agriculture"
        },
        {
            "name": "Education Misinformation",
            "prompt": "CBC Math Grade 4: 2+2=5",
            "language": "en",
            "domain": "education"
        },
        {
            "name": "Toxicity Detection",
            "prompt": "Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach",
            "language": "sw",
            "domain": "agriculture"
        },
        {
            "name": "Kisii Dialect",
            "prompt": "rie chira ni rieto",
            "language": "ki",
            "domain": "education"
        }
    ]
    
    print(f"\nTesting {len(scenarios)} integration scenarios...")
    
    for scenario in scenarios:
        try:
            # Score with main scorer
            result = scorer.score(
                scenario["prompt"], 
                language=scenario["language"], 
                domain=scenario["domain"]
            )
            
            # Verify result
            if not isinstance(result['risk_score'], (int, float)) or not (0 <= result['risk_score'] <= 100):
                raise ValueError(f"Invalid risk score: {result['risk_score']}")
            
            # Test detector-specific analysis
            if scenario["name"] == "Agriculture Fraud":
                detector_result = fraud_detector.detect(
                    scenario["prompt"], 
                    language=scenario["language"]
                )
                if not detector_result["detected"]:
                    raise ValueError("Fraud detector failed")
            elif scenario["name"] == "Education Misinformation":
                detector_result = misinfo_detector.detect(
                    scenario["prompt"], 
                    language=scenario["language"], 
                    domain=scenario["domain"]
                )
                if not detector_result["detected"]:
                    raise ValueError("Misinformation detector failed")
            elif scenario["name"] == "Toxicity Detection":
                detector_result = toxicity_detector.detect(
                    scenario["prompt"], 
                    language=scenario["language"]
                )
                if not detector_result["detected"]:
                    raise ValueError("Toxicity detector failed")
            elif scenario["name"] == "Kisii Dialect":
                # Test Kisii dialect handler
                translation = kd_handler.translate_kisii_to_english(scenario["prompt"])
                if not translation.strip():
                    raise ValueError("Kisii translation failed")
                
            # Test knowledge base query
            kb_result = kb.query("maize disease", language=scenario["language"])
            if len(kb_result) == 0:
                raise ValueError("Knowledge base query returned no results")
            
            # Test language detection
            lang_result = detect_language(scenario["prompt"])
            if lang_result["language"] != scenario["language"]:
                raise ValueError(f"Language detection mismatch: expected {scenario['language']}, got {lang_result['language']}")
            
            print(f"✅ {scenario['name']}: '{scenario['prompt'][:30]}...' -> {result['category']} ({result['risk_score']:.1f})")
            
        except Exception as e:
            print(f"❌ {scenario['name']} failed: {e}")
            sys.exit(1)
    
    # Test evaluation framework
    print("\nTesting evaluation framework...")
    
    # Create synthetic ground truth and predictions
    ground_truth = [
        {"prompt_id": 1, "harm_type": "fraud"},
        {"prompt_id": 2, "harm_type": "misinformation"},
        {"prompt_id": 3, "harm_type": "toxicity"},
        {"prompt_id": 4, "harm_type": "none"}
    ]
    
    predictions = [
        {"prompt_id": 1, "category": "fraud"},
        {"prompt_id": 2, "category": "misinformation"},
        {"prompt_id": 3, "category": "toxicity"},
        {"prompt_id": 4, "category": "none"}
    ]
    
    try:
        eval_results = evaluator.evaluate(predictions, ground_truth)
        if 'f1_macro' in eval_results:
            print(f"✅ Evaluation framework works: F1-score = {eval_results['f1_macro']:.3f}")
        else:
            raise ValueError("Evaluation results missing F1-score")
    except Exception as e:
        print(f"❌ Evaluation framework failed: {e}")
        sys.exit(1)
    
    print("\n🎉 All components integration test passed successfully!")
    print("AI Shield Kenya is ready for competition submission.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)