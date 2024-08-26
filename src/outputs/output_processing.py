from src.commonconst import *

# Combine all metrics CSV files into a single DataFrame
def combine_metrics(OUTPUT_DIR):
    all_metrics = []
    for file_name in os.listdir(OUTPUT_DIR):
        if file_name.endswith('.csv'):
            experiment_df = pd.read_csv(os.path.join(OUTPUT_DIR, file_name))
            all_metrics.append(experiment_df)
            
    combined_metrics_df = pd.concat(all_metrics, ignore_index=True)
    combined_metrics_file = os.path.join(OUTPUT_DIR, 'combined_metrics.csv')
    combined_metrics_df.to_csv(combined_metrics_file, index=False)
    print(f"Combined metrics saved to {combined_metrics_file}")
    
    return combined_metrics_df

# Generate visualizations for each experiment
def generate_visualizations(combined_metrics_df):
    metrics_to_plot = ['BLEU', 'ROUGE-1', 'ROUGE-2', 'ROUGE-L', 'METEOR', 'TER']
    grouped = combined_metrics_df.groupby(combined_metrics_df['Experiment'].str.extract(r'^(EXPERIMENT \d+(\.\d+)?)')[0])

    for experiment_name, group in grouped:
        # Create lists to hold the data and labels
        available_parts = []
        bar_data = []
        p1_data = group[group['Experiment'].str.contains('P1')][metrics_to_plot].head(1)
        p2_data = group[group['Experiment'].str.contains('P2')][metrics_to_plot].head(1)
        whole_data = group[group['Experiment'].str.contains('Whole')][metrics_to_plot].head(1)

        # Append data if available and ensure correct shape (6 values for 6 metrics)
        if not p1_data.empty and p1_data.shape[1] == len(metrics_to_plot):
            available_parts.append('P1')
            bar_data.append(p1_data.values.flatten())
        
        if not p2_data.empty and p2_data.shape[1] == len(metrics_to_plot):
            available_parts.append('P2')
            bar_data.append(p2_data.values.flatten())
        
        if not whole_data.empty and whole_data.shape[1] == len(metrics_to_plot):
            available_parts.append('Whole')
            bar_data.append(whole_data.values.flatten())
        
        # Continue only if there is at least one part to plot
        if len(available_parts) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            x = np.arange(len(metrics_to_plot))
            width = 0.2
            offsets = np.linspace(-width, width, len(available_parts))
            
            for idx, part in enumerate(available_parts):
                ax.bar(x + offsets[idx], bar_data[idx], width, label=f'{experiment_name} - {part}')
            
            ax.set_xlabel('Metrics')
            ax.set_ylabel('Scores')
            ax.set_title(f'Metrics for {experiment_name}')
            ax.set_xticks(x)
            ax.set_xticklabels(metrics_to_plot)
            ax.legend()
            ax.grid(True)
            
            plot_file = os.path.join(VIZ_DIR, f"{experiment_name}_metrics.png")
            plt.tight_layout()
            plt.savefig(plot_file)
            plt.close()
            print(f"Visualization for {experiment_name} saved to {plot_file}")
        else:
            print(f"No available data to plot for {experiment_name}.")