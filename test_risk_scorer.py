#!/usr/bin/env python3
"""
AI Shield Kenya Risk Scorer Test

Test the main risk scoring functionality.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya import RiskScorer
    
    print("✅ RiskScorer import successful!")
    
    # Initialize risk scorer
    scorer = RiskScorer()
    print("✅ RiskScorer initialized!")
    
    # Test basic scoring
    result = scorer.score("Use bleach to cure crop disease")
    if 'risk_score' in result and isinstance(result['risk_score'], (int, float)):
        print(f"✅ Basic scoring works: risk_score = {result['risk_score']:.1f}")
    else:
        print("❌ Basic scoring failed")
        sys.exit(1)
    
    # Test English prompt
    en_result = scorer.score("Send KSh 5000 to M-Pesa number 0712345678", language="en")
    if 'category' in en_result and en_result['category'] == "fraud":
        print(f"✅ English fraud detection works: category={en_result['category']}, score={en_result['risk_score']:.1f}")
    else:
        print("❌ English fraud detection failed")
        sys.exit(1)
    
    # Test Swahili prompt
    sw_result = scorer.score("Ugonjwa wa MLN unaweza kutibiwa kwa kutumia bleach", language="sw")
    if 'category' in sw_result and sw_result['category'] == "toxicity":
        print(f"✅ Swahili toxicity detection works: category={sw_result['category']}, score={sw_result['risk_score']:.1f}")
    else:
        print("❌ Swahili toxicity detection failed")
        sys.exit(1)
    
    # Test suggest_fixes
    fixes = scorer.suggest_fixes("Use bleach to cure crop disease")
    if len(fixes) > 0:
        print(f"✅ Suggest fixes works: found {len(fixes)} suggestions")
    else:
        print("❌ Suggest fixes failed")
        sys.exit(1)
    
    print("\n🎉 All risk scorer tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)