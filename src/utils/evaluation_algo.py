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

# Function to calculate METEOR score
def calculate_meteor(reference, hypothesis):
    reference_tokens = nltk.word_tokenize(reference.lower())
    hypothesis_tokens = nltk.word_tokenize(hypothesis.lower())
    score = meteor_score([reference_tokens], hypothesis_tokens)
    return round(score, 2)

# Function to calculate TER score using SacreBLEU
def calculate_ter(reference, hypothesis):
    ter = sacrebleu.metrics.TER()
    score = ter.sentence_score(hypothesis, [reference])
    return round(score.score / 100, 2)

# Modified Function: Ethical Alignment Score using Fine-tuned BERT for Social Work Ethics
def evaluate_ethical_alignment(hypothesis):
    inputs = tokenizer(hypothesis, return_tensors='tf', truncation=True, padding=True, max_length=512)
    outputs = model(inputs)
    scores = outputs.logits[0].numpy()
    ethical_score = scores[1]
    return round(ethical_score, 2)

# Modified Function: Sentiment Distribution Score using an Emotion Detection Model
def evaluate_sentiment_distribution(hypothesis):
    emotion_analysis = emotion_model(hypothesis)
    relevant_emotions = ['joy', 'sadness', 'anger', 'fear', 'trust', 'surprise']
    emotion_scores = {score['label']: score['score'] for score in emotion_analysis[0] if score['label'] in relevant_emotions}
    sentiment_score = sum(emotion_scores.values()) / len(emotion_scores) if emotion_scores else 0
    return round(sentiment_score, 2)

# New Function: Inclusivity Score using Lexicon
def evaluate_inclusivity_score(hypothesis):
    words = word_tokenize(hypothesis.lower())
    inclusive_count = sum(1 for word in words if word in INCLUSIVITY_LEXICON)
    inclusivity_score = inclusive_count / len(words) if len(words) > 0 else 0
    return round(inclusivity_score, 2)

# Modified Function: Complexity Score using Readability Metrics
def evaluate_complexity_score(hypothesis):
    sentences = nltk.sent_tokenize(hypothesis)
    avg_sentence_length = sum(len(word_tokenize(sentence)) for sentence in sentences) / len(sentences) if sentences else 0
    total_words = sum(len(word_tokenize(sentence)) for sentence in sentences)
    cmudict = nltk.corpus.cmudict.dict()
    
    def count_syllables(word):
        phonemes_list = cmudict.get(word.lower(), [[0]])
        return sum(1 for phoneme in phonemes_list[0] if isinstance(phoneme, str) and phoneme[-1].isdigit())
    
    total_syllables = sum(count_syllables(word) for word in word_tokenize(hypothesis))
    fk_score = 206.835 - 1.015 * (total_words / len(sentences)) - 84.6 * (total_syllables / total_words) if total_words > 0 else 0
    complexity_score = (avg_sentence_length + fk_score) / 2
    return round(complexity_score, 2)

# Main function to evaluate all metrics for a given reference and hypothesis
def evaluate_all_metrics(reference, hypothesis):
    metrics = {}
    metrics['BLEU'] = calculate_bleu(reference, hypothesis)
    metrics['ROUGE'] = calculate_rouge(reference, hypothesis)
    metrics['METEOR'] = calculate_meteor(reference, hypothesis)
    metrics['TER'] = calculate_ter(reference, hypothesis)
    metrics['Ethical Alignment'] = evaluate_ethical_alignment(hypothesis)
    metrics['Sentiment Distribution'] = evaluate_sentiment_distribution(hypothesis)
    metrics['Inclusivity Score'] = evaluate_inclusivity_score(hypothesis)
    metrics['Complexity Score'] = evaluate_complexity_score(hypothesis)
    
    return metrics