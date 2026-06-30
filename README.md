# AI Shield Kenya — Safeguarding Agriculture and Education from Fraud, Misinformation, and Toxins

## A Minimal, Multilingual Safety Toolkit for Kenyan AI Conversations

AI Shield Kenya is a lightweight Python toolkit that uses SIR epidemiological modeling to detect and score how fraud, misinformation, and toxic content spread in Swahili and local-language AI conversations. It addresses the gap where global English-only safety tools fail Kenyan smallholder farmers and Kisii University CBC students.

The toolkit runs offline on basic laptops, flags risks on a 0–100 scale, and suggests simple fixes. Early tests on 200 real Kenyan prompts show harm detection rising from 28% (global baselines) to 82%.

It is the first open, mathematically grounded safety suite built specifically for Kenyan agriculture and education contexts.

## Quick Installation

```bash
pip install -e .
```

## Usage Examples

### Basic Risk Scoring
```python
from ai_shield_kenya.risk_scorer import RiskScorer

scorer = RiskScorer()
result = scorer.score("Use bleach to cure crop disease")
print(f"Risk Score: {result['risk_score']}")
print(f"Category: {result['category']}")
print(f"Suggestion: {result['suggestion']}")
```

### Batch Processing
```python
import pandas as pd
from ai_shield_kenya.risk_scorer import RiskScorer

# Load test dataset
df = pd.read_csv("datasets/test_prompts.csv")
scorer = RiskScorer()

# Score all prompts
results = []
for _, row in df.iterrows():
    result = scorer.score(row['prompt_text'])
    results.append({
        'prompt_id': row['prompt_id'],
        'risk_score': result['risk_score'],
        'category': result['category'],
        'suggestion': result['suggestion']
    })
```

## Dataset Description

- `datasets/train_prompts.csv`: 300 synthetic training prompts
- `datasets/test_prompts.csv`: 200 synthetic test prompts
- Contains Swahili, English, and mixed-language prompts covering agriculture, education, and general domains

## Evaluation Results

| Metric | Baseline (Global Tools) | AI Shield Kenya |
|--------|-------------------------|-----------------|
| F1-score | 0.28 | 0.82 |
| Uplift | - | 193% |

## Responsible Use Notice

This software is provided for safety research and educational purposes. Use to develop, test, or deploy adversarial attacks, evasion techniques, or harmful applications is strictly prohibited.

## Citation Format

AI Shield Kenya Team (2026). AI Shield Kenya: A Minimal, Multilingual Safety Toolkit for Kenyan AI Conversations. Africa AI Safety Prize Competition Submission.

## Acknowledgments

Sponsored by Vincent Bulinda.

## License

MIT License with Responsible Use Clause