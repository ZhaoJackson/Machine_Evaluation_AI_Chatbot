# Import necessary libraries
import os
import random
import re
import sys
import csv
import matplotlib.pyplot as plt
import numpy as np
import nltk
import pandas as pd
import sacrebleu
import spacy
import tensorflow_hub as hub
from docx import Document
from nltk.tokenize import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from nltk.util import ngrams
from rouge_score import rouge_scorer
from textblob import TextBlob
from transformers import pipeline, BertTokenizer, TFBertForSequenceClassification

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# File Paths
DOC_PATH = "src/experiments/data_input.docx"
REFERENCE_CSV_PATH = "src/experiments/reference_text.csv"
EXPERIMENT_CSV_PATH = "src/experiments/experiment_text.csv"
OUTPUT_DIR = os.path.join("src", "outputs", "output_metrics")
VIZ_DIR = os.path.join("src", "outputs", "visualizations")
BERT_MODEL_PATH = os.path.join("models", "bert_text_classification")

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VIZ_DIR, exist_ok=True)

# NLTK Downloads
nltk.download('punkt')
nltk.download('wordnet', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('cmudict')

# Initialize the emotion detection model
emotion_model = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)

# Initialize spaCy model for NER
SPACY_MODEL = 'en_core_web_sm'
nlp = spacy.load(SPACY_MODEL)

# Initialize BERT model and tokenizer for text classification (using TensorFlow version)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertForSequenceClassification.from_pretrained('bert-base-uncased')

# Load the Universal Sentence Encoder (previously used for action-oriented phrases, now omitted)
UNIVERSAL_ENCODER = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

# Constants for target lengths for experiments
P1_TARGET_LENGTH = 85
P2_TARGET_LENGTH = 115
WHOLE_TARGET_LENGTH = 200

# Experiment IDs
EXPERIMENT_IDS = [91, 91.0, 91.1, 91.2, 92.0, 92.1, 92.2]

# Constants for new metrics
ETHICAL_ALIGNMENT_THRESHOLD = 0.5
CULTURAL_SENSITIVITY_LEXICON = set([
    "diversity", "inclusion", "equality", "justice", "community", "multicultural",
    "intersectional", "equity", "non-discriminatory", "cultural sensitivity"
])
INCLUSIVITY_LEXICON = set([
    "they", "them", "their", "non-binary", "LGBTQ+", "accessible", "inclusive", "neurodivergent",
    "underrepresented", "equitable", "affirming"
])

# Utility function to load text data from CSV files
def load_text_data(filepath):
    return pd.read_csv(filepath)

# Function to save results DataFrame to CSV
def save_results_to_csv(result_entries, experiment_name):
    results_df = pd.DataFrame(result_entries)
    output_file = os.path.join(OUTPUT_DIR, f"{experiment_name}.csv")
    results_df.to_csv(output_file, index=False)
    print(f"Metrics for {experiment_name} saved to {output_file}")

# Import functions
from src.experiments.data_processing import process_document_to_csv
from src.utils.text_transform import process_experiment, preprocess_text, generate_ngrams, generate_paragraph_from_ngrams
from src.utils.benchmark import process_experiments
from src.outputs.output_processing import combine_metrics, generate_visualizations

# Visualization settings
PLOTLY_TEMPLATE = "plotly_white"