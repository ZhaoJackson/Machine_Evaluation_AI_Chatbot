# evaluation_algo.py

from src.commonconst import *

# Function to calculate BLEU score with smoothing
def calculate_bleu(reference, hypothesis):
    reference_tokens = [nltk.word_tokenize(reference.lower())]
    hypothesis_tokens = nltk.word_tokenize(hypothesis.lower())
    smoothing_fn = SmoothingFunction().method1
    bleu_score = sentence_bleu(reference_tokens, hypothesis_tokens, smoothing_function=smoothing_fn)
    return round(bleu_score, 2)

# Function to calculate ROUGE score
def calculate_rouge(reference, hypothesis):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {key: {k: round(v, 2) for k, v in score._asdict().items()} for key, score in scores.items()}

def calculate_meteor(reference, hypothesis):
    # Tokenize the reference and hypothesis
    reference_tokens = nltk.word_tokenize(reference.lower())
    hypothesis_tokens = nltk.word_tokenize(hypothesis.lower())
    # Compute the METEOR score with the tokenized inputs
    score = meteor_score([reference_tokens], hypothesis_tokens)
    
    return round(score, 2)

# Function to calculate TER score using SacreBLEU
def calculate_ter(reference, hypothesis):
    ter = sacrebleu.metrics.TER()
    score = ter.sentence_score(hypothesis, [reference])
    return round(score.score / 100, 2)  # TER is returned as a percentage, scaled to 0-1 range

# Function to evaluate all metrics for a given reference and hypothesis
def evaluate_all_metrics(reference, hypothesis):
    metrics = {}
    metrics['BLEU'] = calculate_bleu(reference, hypothesis)
    metrics['ROUGE'] = calculate_rouge(reference, hypothesis)
    metrics['METEOR'] = calculate_meteor(reference, hypothesis)
    metrics['TER'] = calculate_ter(reference, hypothesis)
    
    return metrics