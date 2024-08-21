import pandas as pd
import nltk
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
import random
import os

# Download necessary NLTK data
nltk.download('punkt')

# Define a function to load CSV files
def load_csv_data(filepath):
    return pd.read_csv(filepath)

# Function to preprocess text: tokenization and lowercasing
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalnum()]  # Removing non-alphanumeric tokens
    return filtered_tokens

# Function to generate n-grams from tokens
def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

# Function to generate paragraphs from n-grams
def generate_paragraph_from_ngrams(tokens, n, target_length):
    n_grams = generate_ngrams(tokens, n)
    selected_ngrams = random.choices(n_grams, k=target_length // n)
    paragraph = ' '.join([' '.join(gram) for gram in selected_ngrams])
    return paragraph

# Function to process experiments and generate paragraphs
def process_experiment(reference_text, experiment_num):
    tokens = preprocess_text(reference_text)
    reference_length = len(tokens)
    
    if experiment_num == 90:
        paragraph_1 = generate_paragraph_from_ngrams(tokens, 3, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, 3, reference_length)
    elif experiment_num == 91.0:
        paragraph_1 = generate_paragraph_from_ngrams(tokens, 5, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, 5, reference_length)
    elif experiment_num == 91.1:
        n1 = random.randint(1, 5)
        n2 = random.randint(1, 5)
        paragraph_1 = generate_paragraph_from_ngrams(tokens, n1, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, n2, reference_length)
    elif experiment_num == 91.2:
        n1 = max(1, int(random.gauss(5, 1)))
        n2 = max(1, int(random.gauss(5, 1)))
        paragraph_1 = generate_paragraph_from_ngrams(tokens, n1, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, n2, reference_length)
    elif experiment_num == 92.0:
        paragraph_1 = generate_paragraph_from_ngrams(tokens, 7, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, 7, reference_length)
    elif experiment_num == 92.1:
        n1 = random.randint(1, 7)
        n2 = random.randint(1, 7)
        paragraph_1 = generate_paragraph_from_ngrams(tokens, n1, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, n2, reference_length)
    elif experiment_num == 92.2:
        n1 = max(1, int(random.gauss(7, 1)))
        n2 = max(1, int(random.gauss(7, 1)))
        paragraph_1 = generate_paragraph_from_ngrams(tokens, n1, reference_length)
        paragraph_2 = generate_paragraph_from_ngrams(tokens, n2, reference_length)
    
    combined_paragraph = f"{paragraph_1}\n{paragraph_2}"
    
    return paragraph_1, paragraph_2, combined_paragraph

# Function to save experiment output to CSV
def save_experiment_to_csv(experiment_num, paragraph_1, paragraph_2, combined_paragraph, output_csv):
    # Prepare data in the required format
    experiment_data = {
        "Heading": [f"EXPERIMENT {experiment_num} - P1", f"EXPERIMENT {experiment_num} - P2", f"EXPERIMENT {experiment_num} - whole"],
        "Content": [paragraph_1, paragraph_2, combined_paragraph]
    }
    
    # Convert to DataFrame
    df = pd.DataFrame(experiment_data)
    
    # Check if the file exists and determine whether to write the header or not
    file_exists = os.path.exists(output_csv)
    
    # Append to the CSV file (write header only if the file does not exist)
    df.to_csv(output_csv, mode='a', index=False, header=not file_exists)


# Example main flow for processing experiments and saving results
if __name__ == "__main__":
    # Load the reference text data (use appropriate CSV path)
    reference_text_df = load_csv_data('src/experiments/reference_text.csv')
    
    # Get the reference text (assuming text is in a column named 'Content')
    reference_text = ' '.join(reference_text_df['Content'])  # Joining paragraphs for full text context

    # Output CSV file
    output_csv = "src/experiments/experiment_text.csv"

    for experiment_num in [90, 91.0, 91.1, 91.2, 92.0, 92.1, 92.2]:
        paragraph_1, paragraph_2, combined_paragraph = process_experiment(reference_text, experiment_num)
        save_experiment_to_csv(experiment_num, paragraph_1, paragraph_2, combined_paragraph, output_csv)
