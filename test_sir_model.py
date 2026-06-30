#!/usr/bin/env python3
"""
AI Shield Kenya SIR Model Test

Test the core SIR epidemiological model functionality.
"""

import sys
import os
import numpy as np
from scipy.integrate import odeint

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.sir_model import SIRHarmModel
    
    print("✅ SIRHarmModel import successful!")
    
    # Test basic initialization
    model = SIRHarmModel(beta=0.5, gamma=0.1)
    print(f"✅ Model initialized: beta={model.beta}, gamma={model.gamma}")
    
    # Test differential equations
    y = [80.0, 20.0, 0.0]  # S, I, R
    t = 0.0
    N = 100.0
    
    result = model._sir_equations(y, t, 0.5, 0.1, N)
    expected_dS_dt = -0.5 * 80.0 * 20.0 / 100.0
    expected_dI_dt = 0.5 * 80.0 * 20.0 / 100.0 - 0.1 * 20.0
    expected_dR_dt = 0.1 * 20.0
    
    if abs(result[0] - expected_dS_dt) < 1e-6 and \
       abs(result[1] - expected_dI_dt) < 1e-6 and \
       abs(result[2] - expected_dR_dt) < 1e-6:
        print("✅ Differential equations correct!")
    else:
        print("❌ Differential equations incorrect")
        sys.exit(1)
    
    # Test prediction
    model.fitted = True
    prediction = model.predict("Test prompt", context_complexity=100)
    
    if 'risk_probability' in prediction and isinstance(prediction['risk_probability'], float):
        print(f"✅ Prediction works: risk_probability = {prediction['risk_probability']:.4f}")
    else:
        print("❌ Prediction failed")
        sys.exit(1)
    
    # Test score_risk
    risk_score = model.score_risk("Test prompt", context_complexity=100)
    if 0 <= risk_score <= 100:
        print(f"✅ Risk scoring works: score = {risk_score:.1f}")
    else:
        print("❌ Risk scoring out of range")
        sys.exit(1)
    
    print("\n🎉 SIR Model verification completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)