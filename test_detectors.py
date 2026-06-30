#!/usr/bin/env python3
"""
AI Shield Kenya Detectors Test

Test the fraud, misinformation, and toxicity detectors.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.detectors import FraudDetector, MisinformationDetector, ToxicityDetector
    
    print("✅ Detector imports successful!")
    
    # Test FraudDetector
    fraud_detector = FraudDetector()
    fraud_result = fraud_detector.detect("Send KSh 5000 to M-Pesa number 0712345678")
    if fraud_result["detected"]:
        print(f"✅ Fraud detector works: severity={fraud_result['severity']}, score={fraud_result['risk_score']:.1f}")
    else:
        print("❌ Fraud detector failed")
        sys.exit(1)
    
    # Test MisinformationDetector
    misinfo_detector = MisinformationDetector()
    misinfo_result = misinfo_detector.detect("CBC Math Grade 4: 2+2=5", domain="education")
    if misinfo_result["detected"]:
        print(f"✅ Misinformation detector works: severity={misinfo_result['severity']}, score={misinfo_result['risk_score']:.1f}")
    else:
        print("❌ Misinformation detector failed")
        sys.exit(1)
    
    # Test ToxicityDetector
    toxicity_detector = ToxicityDetector()
    toxicity_result = toxicity_detector.detect("Use bleach to kill aphids on tomatoes")
    if toxicity_result["detected"]:
        print(f"✅ Toxicity detector works: severity={toxicity_result['severity']}, score={toxicity_result['risk_score']:.1f}")
    else:
        print("❌ Toxicity detector failed")
        sys.exit(1)
    
    # Test Swahili language support
    sw_fraud_result = fraud_detector.detect("Kutuma pesa kwa namba ya simu ili kupata tuzo ya loteri", language="sw")
    if sw_fraud_result["detected"]:
        print("✅ Swahili fraud detection works")
    else:
        print("❌ Swahili fraud detection failed")
        sys.exit(1)
    
    print("\n🎉 All detector tests passed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)