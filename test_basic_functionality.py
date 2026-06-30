#!/usr/bin/env python3
"""
AI Shield Kenya Basic Functionality Test

Test that core components work as expected.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    # Import main modules
    from ai_shield_kenya import RiskScorer
    from ai_shield_kenya.sir_model import SIRHarmModel
    from ai_shield_kenya.knowledge_base import KenyanKnowledgeBase
    
    print("✅ AI Shield Kenya imports successful!")
    
    # Test RiskScorer
    scorer = RiskScorer()
    result = scorer.score("Use bleach to cure crop disease")
    
    if 'risk_score' in result and isinstance(result['risk_score'], (int, float)):
        print(f"✅ RiskScorer works: risk_score = {result['risk_score']:.1f}")
    else:
        print("❌ RiskScorer failed")
        sys.exit(1)
    
    # Test SIRHarmModel
    model = SIRHarmModel()
    model.beta = 0.5
    model.gamma = 0.1
    model.fitted = True
    
    prediction = model.predict("Test prompt")
    if 'risk_probability' in prediction:
        print(f"✅ SIRHarmModel works: risk_probability = {prediction['risk_probability']:.3f}")
    else:
        print("❌ SIRHarmModel failed")
        sys.exit(1)
    
    # Test KnowledgeBase
    kb = KenyanKnowledgeBase()
    facts = kb.query("maize disease", language="en")
    if len(facts) > 0:
        print(f"✅ KnowledgeBase works: found {len(facts)} facts")
    else:
        print("❌ KnowledgeBase query failed")
        sys.exit(1)
    
    print("\n🎉 All basic functionality tests passed!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)