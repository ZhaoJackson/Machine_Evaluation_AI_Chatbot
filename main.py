from src.commonconst import *

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    # Process the document and generate CSV files from the original experiments
    process_document_to_csv(
        doc_path=DOC_PATH,
        reference_csv_path=REFERENCE_CSV_PATH,
        experiment_csv_path=EXPERIMENT_CSV_PATH
    )
    print("Original data processing complete. CSV files generated successfully.")

    # Load experiment data
    experiment_data = pd.read_csv(EXPERIMENT_CSV_PATH)
    
    # Process experiments from 91 to 92.2
    processed_data = []
    for experiment_num in EXPERIMENT_IDS:
        reference_text = experiment_data.iloc[0]["Content"]
        processed_experiment = process_experiment(reference_text, experiment_num)

        processed_data.append([f"EXPERIMENT {experiment_num} - P1", processed_experiment['P1']])
        processed_data.append([f"EXPERIMENT {experiment_num} - P2", processed_experiment['P2']])
        processed_data.append([f"EXPERIMENT {experiment_num} - Whole", processed_experiment['Whole']])

    # Write new data to CSV
    with open(EXPERIMENT_CSV_PATH, mode='a', newline='', encoding='utf-8') as exp_file:
        writer = csv.writer(exp_file)
        writer.writerows(processed_data)

    print(f"New experiment results saved to {EXPERIMENT_CSV_PATH}")

    # Run the process_experiments function from benchmark
    process_experiments()

if __name__ == "__main__":
    main()