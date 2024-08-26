# commonconst.py

# Import necessary libraries
import pandas as pd
import nltk
import random
import os
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from docx import Document
import csv
import re
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import sacrebleu
import sys
import os

# File Paths
DOC_PATH = "src/experiments/data_input.docx"
REFERENCE_CSV_PATH = "src/experiments/reference_text.csv"
EXPERIMENT_CSV_PATH = "src/experiments/experiment_text.csv"
OUTPUT_DIR = os.path.join("src", "outputs", "output_metrics")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# NLTK Downloads
nltk.download('punkt')
nltk.download('wordnet', quiet=True)

# Constants for target lengths for experiments 91 to 92.2
P1_TARGET_LENGTH = 85
P2_TARGET_LENGTH = 115
WHOLE_TARGET_LENGTH = 200

# Experiment IDs
EXPERIMENT_IDS = [91, 91.0, 91.1, 91.2, 92.0, 92.1, 92.2]

# Utility function to load text data from CSV files
def load_text_data(filepath):
    return pd.read_csv(filepath)

# Function to save results DataFrame to CSV
def save_results_to_csv(result_entries, experiment_name):
    results_df = pd.DataFrame(result_entries)
    output_file = os.path.join(OUTPUT_DIR, f"{experiment_name}.csv")
    results_df.to_csv(output_file, index=False)
    print(f"Metrics for {experiment_name} saved to {output_file}")

# Import functions from data_processing.py and text_transform.py
from src.experiments.data_processing import process_document_to_csv
from src.utils.text_transform import process_experiment, preprocess_text, generate_ngrams, generate_paragraph_from_ngrams
from src.utils.benchmark import process_experiments