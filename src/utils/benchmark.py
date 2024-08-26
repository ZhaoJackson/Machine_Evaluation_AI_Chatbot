# benchmark.py

from src.commonconst import *
from src.utils.evaluation_algo import evaluate_all_metrics

def process_experiments():
    reference_df = load_text_data(REFERENCE_CSV_PATH)
    experiment_df = load_text_data(EXPERIMENT_CSV_PATH)
    
    # Group experiments by their "Heading" (e.g., P1, P2, Whole)
    experiment_groups = experiment_df.groupby(experiment_df['Heading'].str.extract(r'^(EXPERIMENT \d+(\.\d+)?)')[0])

    for experiment_name, group in experiment_groups:
        result_entries = []
        # Extract parts P1, P2, Whole for each experiment
        for part in ['P1', 'P2', 'Whole']:
            experiment_row = group[group['Heading'].str.contains(part)]
            reference_row = reference_df[reference_df['Heading'].str.contains(part)]
            
            if not experiment_row.empty and not reference_row.empty:
                hypothesis_text = experiment_row['Content'].values[0]
                reference_text = reference_row['Content'].values[0]
                
                # Evaluate the metrics
                metrics = evaluate_all_metrics(reference_text, hypothesis_text)
                
                result_entry = {
                    'Experiment': f"{experiment_name} - {part}",
                    'BLEU': metrics['BLEU'],
                    'ROUGE-1': metrics['ROUGE']['rouge1']['fmeasure'],
                    'ROUGE-2': metrics['ROUGE']['rouge2']['fmeasure'],
                    'ROUGE-L': metrics['ROUGE']['rougeL']['fmeasure'],
                    'METEOR': metrics['METEOR'],
                    'TER': metrics['TER']
                }
                result_entries.append(result_entry)

        # Save the results using the common save function
        save_results_to_csv(result_entries, experiment_name)