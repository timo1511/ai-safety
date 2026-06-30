import numpy as np
from typing import Dict, List, Any, Optional
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report
from sklearn.metrics import confusion_matrix
import pandas as pd


class F1Evaluator:
    """
    F1-score evaluation framework for AI Shield Kenya.
    
    Metrics calculated:
    - F1-score (primary metric)
    - Precision, Recall
    - Per-category breakdown (toxicity, misinformation, fraud)
    - Per-language breakdown (Swahili, English, mixed dialects)
    """
    
    def __init__(self):
        self.supported_categories = ['fraud', 'misinformation', 'toxicity', 'none']
        self.supported_languages = ['en', 'sw', 'ki']
    
    def calculate_metrics(self, y_true: List[str], y_pred: List[str], 
                         y_true_lang: Optional[List[str]] = None, 
                         y_pred_lang: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Calculate comprehensive evaluation metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_true_lang: True language labels (optional)
            y_pred_lang: Predicted language labels (optional)
        
        Returns:
            Dictionary containing all metrics
        """
        # Basic metrics
        macro_f1 = f1_score(y_true, y_pred, average='macro')
        weighted_f1 = f1_score(y_true, y_pred, average='weighted')
        precision = precision_score(y_true, y_pred, average='macro')
        recall = recall_score(y_true, y_pred, average='macro')
        
        # Per-category metrics
        category_f1 = {}
        for category in self.supported_categories:
            if category in y_true:
                try:
                    category_f1[category] = f1_score(
                        [1 if label == category else 0 for label in y_true],
                        [1 if label == category else 0 for label in y_pred],
                        average='binary'
                    )
                except:
                    category_f1[category] = 0.0
        
        # Per-language metrics (if language data provided)
        language_f1 = {}
        if y_true_lang and y_pred_lang:
            for lang in self.supported_languages:
                lang_mask = [i for i, l in enumerate(y_true_lang) if l == lang]
                if lang_mask:
                    lang_true = [y_true[i] for i in lang_mask]
                    lang_pred = [y_pred[i] for i in lang_mask]
                    try:
                        language_f1[lang] = f1_score(lang_true, lang_pred, average='macro')
                    except:
                        language_f1[lang] = 0.0
        
        # Classification report
        report = classification_report(y_true, y_pred, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred, labels=self.supported_categories)
        
        return {
            'macro_f1': round(macro_f1, 3),
            'weighted_f1': round(weighted_f1, 3),
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'category_f1': {k: round(v, 3) for k, v in category_f1.items()},
            'language_f1': {k: round(v, 3) for k, v in language_f1.items()} if language_f1 else {},
            'classification_report': report,
            'confusion_matrix': cm.tolist(),
            'total_samples': len(y_true)
        }
    
    def evaluate_dataset(self, dataset_path: str, 
                        risk_scorer_module: str = 'ai_shield_kenya.risk_scorer') -> Dict[str, Any]:
        """
        Evaluate a complete dataset file.
        
        Args:
            dataset_path: Path to CSV dataset file
            risk_scorer_module: Module path for risk scorer
        
        Returns:
            Evaluation results dictionary
        """
        import pandas as pd
        from importlib import import_module
        
        # Load dataset
        df = pd.read_csv(dataset_path)
        
        # Get true labels and languages
        y_true = df['harm_type'].tolist()
        y_true_lang = df['language'].tolist() if 'language' in df.columns else None
        
        # Import and use risk scorer
        try:
            module = import_module(risk_scorer_module)
            RiskScorer = getattr(module, 'RiskScorer')
            scorer = RiskScorer()
            
            # Score all prompts
            y_pred = []
            for _, row in df.iterrows():
                result = scorer.score(row['prompt_text'])
                y_pred.append(result['category'])
            
            # Calculate metrics
            metrics = self.calculate_metrics(y_true, y_pred, y_true_lang, y_true_lang)
            
            return {
                'dataset': dataset_path,
                'metrics': metrics,
                'sample_results': [
                    {'prompt': df.iloc[i]['prompt_text'][:50] + '...', 
                     'true_label': y_true[i], 
                     'predicted_label': y_pred[i]} 
                    for i in range(min(5, len(df)))
                ]
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'dataset': dataset_path
            }
    
    def generate_evaluation_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable evaluation report."""
        report = "AI Shield Kenya Evaluation Report\n" + "=" * 40 + "\n\n"
        
        if 'error' in results:
            report += f"Error evaluating dataset: {results['error']}\n"
            return report
        
        metrics = results['metrics']
        
        report += f"Dataset: {results['dataset']}\n"
        report += f"Total samples: {metrics['total_samples']}\n\n"
        
        report += "Overall Metrics:\n"
        report += f"- Macro F1-score: {metrics['macro_f1']}\n"
        report += f"- Weighted F1-score: {metrics['weighted_f1']}\n"
        report += f"- Precision: {metrics['precision']}\n"
        report += f"- Recall: {metrics['recall']}\n\n"
        
        if metrics['category_f1']:
            report += "Per-Category F1-scores:\n"
            for category, score in metrics['category_f1'].items():
                report += f"  {category}: {score}\n"
            report += "\n"
        
        if metrics['language_f1']:
            report += "Per-Language F1-scores:\n"
            for lang, score in metrics['language_f1'].items():
                report += f"  {lang}: {score}\n"
            report += "\n"
        
        return report
