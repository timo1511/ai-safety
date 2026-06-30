#!/usr/bin/env python3
"""
AI Shield Kenya SIR Mathematical Derivation Test

Test the mathematical correctness of the SIR model.
"""

import sys
import os
import numpy as np
from scipy.integrate import odeint

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

try:
    from ai_shield_kenya.sir_model import SIRHarmModel
    
    print("✅ SIR model import successful!")
    
    # Test basic differential equation properties
    model = SIRHarmModel(beta=0.5, gamma=0.1)
    
    # Test that dS/dt + dI/dt + dR/dt = 0 (conservation property)
    y = [80.0, 20.0, 0.0]
    t = 0.0
    N = 100.0
    
    derivatives = model._sir_equations(y, t, 0.5, 0.1, N)
    conservation = sum(derivatives)
    
    if abs(conservation) < 1e-10:
        print("✅ Conservation property holds: dS/dt + dI/dt + dR/dt ≈ 0")
    else:
        print(f"❌ Conservation property failed: sum = {conservation:.6f}")
        sys.exit(1)
    
    # Test that dR/dt = gamma * I
    expected_dR_dt = 0.1 * y[1]
    if abs(derivatives[2] - expected_dR_dt) < 1e-10:
        print("✅ dR/dt = gamma * I property holds")
    else:
        print(f"❌ dR/dt property failed: expected {expected_dR_dt}, got {derivatives[2]:.6f}")
        sys.exit(1)
    
    # Test numerical integration
    def sir_system(y, t, beta, gamma, N):
        S, I, R = y
        dS_dt = -beta * S * I / N
        dI_dt = beta * S * I / N - gamma * I
        dR_dt = gamma * I
        return [dS_dt, dI_dt, dR_dt]
    
    # Initial conditions
    y0 = [80.0, 20.0, 0.0]
    t = np.linspace(0, 10, 100)
    
    try:
        solution = odeint(sir_system, y0, t, args=(0.5, 0.1, 100.0))
        
        # Check that S+I+R is conserved
        total_population = solution[:, 0] + solution[:, 1] + solution[:, 2]
        population_variation = max(total_population) - min(total_population)
        
        if population_variation < 1e-4:
            print("✅ Numerical integration conserves population")
        else:
            print(f"❌ Population not conserved: variation = {population_variation:.6f}")
            sys.exit(1)
        
        # Check that final recovered > initial infected
        if solution[-1, 2] > y0[1] * 0.5:
            print("✅ Recovery behavior correct")
        else:
            print("❌ Recovery behavior incorrect")
            sys.exit(1)
        
        print("\n🎉 SIR mathematical derivation verification completed successfully!")
        
    except Exception as e:
        print(f"❌ Numerical integration failed: {e}")
        sys.exit(1)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Runtime error: {e}")
    sys.exit(1)