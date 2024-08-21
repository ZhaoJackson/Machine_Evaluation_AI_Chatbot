import pandas as pd
import os
from evaluation_algo import evaluate_all_metrics

# Ensure the output directory exists
output_dir = os.path.join("src", "outputs", "output_metrics")
os.makedirs(output_dir, exist_ok=True)

# Function to load text data from CSV files
def load_text_data(filepath):
    return pd.read_csv(filepath)

# Function to process and evaluate metrics for each group of experiments
def process_experiments(reference_file, experiment_file):
    reference_df = load_text_data(reference_file)
    experiment_df = load_text_data(experiment_file)
    
    results = []

    # Group experiments by their "Heading" (e.g., P1, P2, Whole)
    experiment_groups = experiment_df.groupby(experiment_df['Heading'].str.extract(r'^(EXPERIMENT \d+(\.\d+)?)')[0])

    for experiment_name, group in experiment_groups:
        result_entries = []
        # Extract parts P1, P2, Whole for each experiment
        for i, part in enumerate(['P1', 'P2', 'Whole']):
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

        # Convert to DataFrame and save results for each experiment
        results_df = pd.DataFrame(result_entries)
        output_file = os.path.join(output_dir, f"{experiment_name}.csv")
        results_df.to_csv(output_file, index=False)
        print(f"Metrics for {experiment_name} saved to {output_file}")

if __name__ == "__main__":
    # Reference and experiment file paths
    reference_file = 'src/experiments/reference_text.csv'  # Adjust with your actual reference file path
    experiment_file = 'src/experiments/experiment_text.csv'  # Combined experiment text file

    # Process experiments and generate output CSVs for each experiment group
    process_experiments(reference_file, experiment_file)
