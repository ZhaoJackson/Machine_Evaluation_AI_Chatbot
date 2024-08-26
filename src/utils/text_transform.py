from src.commonconst import *

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word.isalnum()]
    return filtered_tokens

def generate_ngrams(tokens, n):
    return list(ngrams(tokens, n))

def generate_paragraph_from_ngrams(tokens, n, target_length):
    n_grams = generate_ngrams(tokens, n)
    selected_ngrams = random.choices(n_grams, k=target_length // n)
    paragraph = ' '.join([' '.join(gram) for gram in selected_ngrams])
    return paragraph

def process_experiment(reference_text, experiment_num):
    tokens = preprocess_text(reference_text)
    
    n1 = n2 = 3
    if experiment_num == 91.0:
        n1 = n2 = 5
    elif experiment_num == 91.1:
        n1 = random.randint(1, 5)
        n2 = random.randint(1, 5)
    elif experiment_num == 91.2:
        n1 = max(1, int(random.gauss(5, 1)))
        n2 = max(1, int(random.gauss(5, 1)))
    elif experiment_num == 92.0:
        n1 = n2 = 4
    elif experiment_num == 92.1:
        n1 = n2 = 2
    
    paragraph_1 = generate_paragraph_from_ngrams(tokens, n1, P1_TARGET_LENGTH)
    paragraph_2 = generate_paragraph_from_ngrams(tokens, n2, P2_TARGET_LENGTH)
    
    return {
        "P1": paragraph_1,
        "P2": paragraph_2,
        "Whole": f"{paragraph_1} {paragraph_2}"
    }