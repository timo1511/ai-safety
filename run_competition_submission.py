#!/usr/bin/env python3
"""
AI Shield Kenya Competition Submission Script

Generate the complete competition submission package.
"""

import sys
import os
import subprocess
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    print("🚀 AI Shield Kenya Competition Submission Generator")
    print("=" * 50)
    
    # Run tests
    print("\n1. Running unit tests...")
    try:
        result = subprocess.run(["python", "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✅ Unit tests passed!")
        else:
            print("❌ Unit tests failed:")
            print(result.stdout)
            print(result.stderr)
            return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1
    
    # Run evaluation
    print("\n2. Running evaluation on test dataset...")
    try:
        result = subprocess.run([
            "python", "scripts/run_evaluation.py", 
            "--test-set", "datasets/test_prompts.csv",
            "--output", "results/",
            "--verbose"
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Evaluation completed successfully!")
        else:
            print("❌ Evaluation failed:")
            print(result.stdout)
            print(result.stderr)
            return 1
    except Exception as e:
        print(f"❌ Error running evaluation: {e}")
        return 1
    
    # Generate report
    print("\n3. Generating competition submission report...")
    try:
        result = subprocess.run([
            "python", "scripts/generate_report.py",
            "--metrics", "results/evaluation_metrics.csv",
            "--output", "competition_submission.pdf",
            "--verbose"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Report generation completed!")
        else:
            print("❌ Report generation failed:")
            print(result.stdout)
            print(result.stderr)
            return 1
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return 1
    
    # Verify results
    print("\n4. Verifying competition claims...")
    try:
        import pandas as pd
        metrics_df = pd.read_csv("results/evaluation_metrics.csv")
        metrics = {}
        for _, row in metrics_df.iterrows():
            metrics[row['metric']] = row['value']
        
        f1_score = metrics.get('f1_macro', 0.0)
        baseline_f1 = 0.28
        uplift = ((f1_score - baseline_f1) / baseline_f1) * 100
        
        print(f"   Baseline F1-score: {baseline_f1:.3f}")
        print(f"   AI Shield Kenya F1-score: {f1_score:.3f}")
        print(f"   Uplift: {uplift:.1f}%")
        
        if f1_score >= 0.82 and uplift >= 193:
            print("✅ All competition requirements met!")
        else:
            print("❌ Some competition requirements not met")
            return 1
            
    except Exception as e:
        print(f"❌ Error verifying results: {e}")
        return 1
    
    # Final summary
    print("\n🎉 AI Shield Kenya Competition Submission Ready!")
    print("\nGenerated files:")
    print("- competition_submission.pdf (main submission document)")
    print("- competition_submission.md (markdown version)")
    print("- results/evaluation_metrics.csv (detailed metrics)")
    print("- results/performance_report.md (performance summary)")
    print("- README.md (project documentation)")
    print("- LICENSE (license information)")
    
    print("\nTo submit:")
    print("1. Upload the entire repository to GitHub")
    print("2. Export competition_submission.pdf from Airtable")
    print("3. Complete the Airtable template with all required information")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())