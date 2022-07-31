import re
import numpy as np
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from string import punctuation
from sklearn.base import BaseEstimator, TransformerMixin


rus_stop_words = stopwords.words('russian')     # List of russian stop words
analyzer = MorphAnalyzer()  # Morphological analyzer that is used for the preprocessing


def remove_emoji(text: str) -> str:
    """Deletes all emoji symbols from raw text"""
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def analyze_text(text: str):
    """Analyzes raw text, makes tokenization and normalizes words"""
    # Removing emojies
    text = remove_emoji(text)
    # Replacing tg links
    text = re.sub(r'\B@\S*', '', text)
    # Deleting nums
    text = re.sub(r'\b\d+\b', '', text)
    # Tokenization
    tok_text = word_tokenize(text)
    # Removing stop words and punctuation
    cleaned_tokens = [token for token in tok_text if token not in rus_stop_words + list(punctuation)]
    # Normalization
    norm_tokens = [analyzer.parse(token)[0].normal_form for token in cleaned_tokens]

    return norm_tokens


class TGLinkTransformer(BaseEstimator, TransformerMixin):
    """Transformer class that can be used in Sklearn preprocessing
       pipeline for deleting telegram links"""
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.array([re.search(r'\B@\S*', text) is not None for text in X]).reshape(-1, 1)
