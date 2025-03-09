from src.commonconst import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    # Step 1: Data Processing (data_processing.py)
    process_document_to_csv(
        doc_path=DOC_PATH,
        reference_csv_path=REFERENCE_CSV_PATH,
        experiment_csv_path=EXPERIMENT_CSV_PATH
    )
    print("Original data processing complete. CSV files generated successfully.")

    # Step 2: Text Transformation (text_transform.py)
    experiment_data = pd.read_csv(EXPERIMENT_CSV_PATH)
    processed_data = []
    
    for experiment_num in EXPERIMENT_IDS:
        reference_text = experiment_data.iloc[0]["Content"]
        processed_experiment = process_experiment(reference_text, experiment_num)
        processed_data.append([f"EXPERIMENT {experiment_num} - P1", processed_experiment['P1']])
        processed_data.append([f"EXPERIMENT {experiment_num} - P2", processed_experiment['P2']])
        processed_data.append([f"EXPERIMENT {experiment_num} - Whole", processed_experiment['Whole']])

    # Append new experiment results to the experiment CSV file
    with open(EXPERIMENT_CSV_PATH, mode='a', newline='', encoding='utf-8') as exp_file:
        writer = csv.writer(exp_file)
        writer.writerows(processed_data)

    print(f"New experiment results saved to {EXPERIMENT_CSV_PATH}")

    # Step 3: Benchmarking (benchmark.py)
    process_experiments()
    print("Benchmarking complete. Results saved to the output directory.")

    # Step 4: Output Processing and Visualization (output_processing.py)
    combined_metrics_df = combine_metrics(OUTPUT_DIR)
    generate_visualizations(combined_metrics_df)
    print("Output processing and visualizations complete.")

if __name__ == "__main__":
    main()