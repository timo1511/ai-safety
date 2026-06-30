#!/usr/bin/env python3
"""
AI Shield Kenya Installation Test Script

Verify that the package installs and imports correctly.
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
    
    # Test basic functionality
    scorer = RiskScorer()
    result = scorer.score("Test prompt")
    
    if 'risk_score' in result and isinstance(result['risk_score'], (int, float)):
        print(f"✅ Basic scoring works: risk_score = {result['risk_score']:.1f}")
    else:
        print("❌ Basic scoring failed")
        sys.exit(1)
    
    # Test knowledge base
    kb = KenyanKnowledgeBase()
    facts = kb.query("maize disease", language="en")
    if len(facts) > 0:
        print(f"✅ Knowledge base query works: found {len(facts)} facts")
    else:
        print("❌ Knowledge base query failed")
        sys.exit(1)
    
    print("\n🎉 AI Shield Kenya installation verification completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)