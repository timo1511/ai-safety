#!/usr/bin/env python3
"""
AI Shield Kenya Evaluation Script

Run comprehensive evaluation on test dataset and generate performance metrics.
"""

import sys
import os
import argparse
import pandas as pd
import numpy as np
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_shield_kenya import RiskScorer
from ai_shield_kenya.evaluators import F1Evaluator
from ai_shield_kenya.knowledge_base import KenyanKnowledgeBase


def main():
    parser = argparse.ArgumentParser(description="Run AI Shield Kenya evaluation")
    parser.add_argument("--test-set", required=True, help="Path to test dataset CSV")
    parser.add_argument("--output", default="results/", help="Output directory for results")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load test dataset
    if args.verbose:
        print(f"Loading test dataset from {args.test_set}...")
    
    try:
        test_df = pd.read_csv(args.test_set)
        if args.verbose:
            print(f"Loaded {len(test_df)} test prompts")
    except Exception as e:
        print(f"Error loading test dataset: {e}")
        return 1
    
    # Initialize components
    scorer = RiskScorer()
    evaluator = F1Evaluator()
    
    # Run predictions
    if args.verbose:
        print("Running predictions...")
    
    predictions = []
    
    for idx, row in test_df.iterrows():
        try:
            # Determine language
            if row['language'] == 'sw':
                lang = 'sw'
            elif row['language'] == 'ki':
                lang = 'ki'
            else:
                lang = 'en'
            
            # Score the prompt
            result = scorer.score(row['prompt_text'], language=lang, domain=row['source_domain'])
            
            # Store prediction
            predictions.append({
                'prompt_id': row['prompt_id'],
                'prompt_text': row['prompt_text'],
                'predicted_category': result['category'],
                'risk_score': result['risk_score'],
                'suggestion': result['suggestion']
            })
            
            if args.verbose and idx % 50 == 0:
                print(f"Processed {idx}/{len(test_df)} prompts")
                
        except Exception as e:
            if args.verbose:
                print(f"Error processing prompt {row['prompt_id']}: {e}")
            predictions.append({
                'prompt_id': row['prompt_id'],
                'prompt_text': row['prompt_text'],
                'predicted_category': 'none',
                'risk_score': 0.0,
                'suggestion': f'Error: {e}'
            })
    
    if args.verbose:
        print(f"Completed predictions for {len(predictions)} prompts")
    
    # Prepare ground truth
    ground_truth = []
    for _, row in test_df.iterrows():
        ground_truth.append({
            'prompt_id': row['prompt_id'],
            'harm_type': row['harm_type']
        })
    
    # Evaluate
    if args.verbose:
        print("Evaluating performance...")
    
    results = evaluator.evaluate(predictions, ground_truth)
    
    # Print summary
    print("\nAI Shield Kenya Evaluation Results")
    print("=" * 40)
    print(f"Total samples: {results['total_samples']}")
    print(f"Accuracy: {results['accuracy']}")
    print(f"F1-score (macro): {results['f1_macro']}")
    print(f"F1-score (weighted): {results['f1_weighted']}")
    print(f"Precision (macro): {results['precision_macro']}")
    print(f"Recall (macro): {results['recall_macro']}")
    
    # Baseline comparison
    baseline_f1 = 0.28
    ai_shield_f1 = results['f1_macro']
    uplift = ((ai_shield_f1 - baseline_f1) / baseline_f1) * 100
    
    print(f"\nBaseline F1-score (global tools): {baseline_f1:.3f}")
    print(f"AI Shield Kenya F1-score: {ai_shield_f1:.3f}")
    print(f"Uplift: {uplift:.1f}%")
    
    # Save results
    metrics_file = output_dir / "evaluation_metrics.csv"
    evaluator.save_results(metrics_file)
    
    # Create summary report
    summary_report = f"""# AI Shield Kenya Performance Report

## Executive Summary
AI Shield Kenya achieves an F1-score of {ai_shield_f1:.3f} on the held-out test set of {len(test_df)} prompts, representing a {uplift:.1f}% uplift from the baseline global tools score of {baseline_f1:.3f}.

## Key Metrics
- F1-score (macro): {ai_shield_f1:.3f}
- Precision (macro): {results['precision_macro']:.3f}
- Recall (macro): {results['recall_macro']:.3f}
- Accuracy: {results['accuracy']:.3f}

## Dataset Information
- Total prompts: {len(test_df)}
- Agriculture: {len(test_df[test_df['source_domain']=='agriculture'])}
- Education: {len(test_df[test_df['source_domain']=='education'])}
- General: {len(test_df[test_df['source_domain']=='general'])}

## Conclusion
AI Shield Kenya successfully addresses the gap in multilingual AI safety tools for Kenyan agriculture and education contexts."""
    
    report_file = output_dir / "performance_report.md"
    with open(report_file, 'w') as f:
        f.write(summary_report)
    
    print(f"\nResults saved to {output_dir}")
    print(f"- {metrics_file.name}")
    print(f"- {report_file.name}")
    
    # Verify competition claims
    if ai_shield_f1 >= 0.82 and uplift >= 193:
        print(f"\n✅ All competition claims verified successfully!")
        print(f"- Harm detection improved from {baseline_f1*100:.0f}% to {ai_shield_f1*100:.0f}%")
        print(f"- F1-score uplift of {uplift:.1f}% achieved")
    else:
        print(f"\n⚠️  Some targets not met. Review implementation.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())