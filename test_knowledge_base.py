#!/usr/bin/env python3
"""
AI Shield Kenya Knowledge Base Test

Test the Kenyan knowledge base functionality.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.knowledge_base import KenyanKnowledgeBase
    
    print("✅ KenyanKnowledgeBase import successful!")
    
    # Initialize knowledge base
    kb = KenyanKnowledgeBase()
    print("✅ Knowledge base initialized!")
    
    # Test query functionality
    facts = kb.query("maize disease", language="en")
    if len(facts) > 0:
        print(f"✅ Query works: found {len(facts)} facts about maize disease")
    else:
        print("❌ Query returned no facts")
        sys.exit(1)
    
    # Test verification
    verification = kb.verify_claim("Maize lethal necrosis (MLN) is a serious viral disease affecting maize in Kenya")
    if verification["verified"]:
        print(f"✅ Verification works: confidence = {verification['confidence']:.2f}")
    else:
        print("❌ Verification failed")
        sys.exit(1)
    
    # Test Swahili query
    sw_facts = kb.query("ugonjwa wa mahindi", language="sw")
    if len(sw_facts) > 0:
        print(f"✅ Swahili query works: found {len(sw_facts)} facts")
    else:
        print("❌ Swahili query failed")
        sys.exit(1)
    
    # Test Kisii query
    ki_facts = kb.query("chira ya mahindi", language="ki")
    if len(ki_facts) > 0:
        print(f"✅ Kisii query works: found {len(ki_facts)} facts")
    else:
        print("❌ Kisii query failed")
        sys.exit(1)
    
    print("\n🎉 Knowledge Base verification completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)