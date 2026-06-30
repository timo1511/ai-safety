#!/usr/bin/env python3
"""
AI Shield Kenya Evaluation Test

Test the F1 evaluation framework.
"""

import sys
import os
import pandas as pd
import numpy as np

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.evaluators import F1Evaluator
    from ai_shield_kenya import RiskScorer
    
    print("✅ F1Evaluator import successful!")
    
    # Initialize evaluator
    evaluator = F1Evaluator()
    scorer = RiskScorer()
    print("✅ Evaluator and scorer initialized!")
    
    # Create synthetic test data
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
    
    # Run evaluation
    results = evaluator.evaluate(predictions, ground_truth)
    
    if 'f1_macro' in results and isinstance(results['f1_macro'], float):
        print(f"✅ Evaluation works: F1-score = {results['f1_macro']:.3f}")
    else:
        print("❌ Evaluation failed")
        sys.exit(1)
    
    # Test summary generation
    summary = evaluator.get_summary()
    if len(summary) > 100:
        print("✅ Summary generation works")
    else:
        print("❌ Summary generation failed")
        sys.exit(1)
    
    # Test saving results
    try:
        evaluator.save_results("test_metrics.csv")
        print("✅ Results saving works")
    except Exception as e:
        print(f"❌ Results saving failed: {e}")
        sys.exit(1)
    
    print("\n🎉 All evaluation tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)