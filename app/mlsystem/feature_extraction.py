import numpy as np
import nltk
from nltk.util import ngrams
from collections import Counter
from stanfordcorenlp import StanfordCoreNLP
import spacy
import json
from sklearn.feature_extraction.text import TfidfVectorizer



STANFORD_MODEL_PATH = 'models/stanford-corenlp-full-2016-10-31'
SPACY_MODEL = 'en_core_web_md'


SENTENCES = "sentences"
SENTIMENT = "sentiment"
SENTIMENT_VALUE = "sentimentValue"
SENTIMENT_ANNOTATOR = {'annotators':'sentiment', 'pipelineLanguage':'en', 'outputFormat':'json'}
SENTIMENT_INDEX = {"Positive": 0,
                    "Neutral": 1,
                    "Negative": 2,
                    "Verynegative":3}


NGRAM_SIZE = 100

MAX_DF = 0.8
MIN_DF = 5
MAX_FEATURES = 2000

class Features:
    def __init__(self):
        self.stanford_nlp = StanfordCoreNLP(STANFORD_MODEL_PATH)
        self.spacy_nlp = spacy.load(SPACY_MODEL)
        self.tfidf = TfidfVectorizer(min_df = MIN_DF,
                            max_df = MAX_DF,
                            max_features = MAX_FEATURES,
                            stop_words = 'english',
                            norm = 'l2'
                            )

    def get_features(self, t, is_train):
        doc_vocab_mat,lookup = self._get_tfidf(t, is_train)
        bigram_counts = self._get_ngram_counts(t, 2)
        trigram_counts = self._get_ngram_counts(t, 3)

        sentiments = self._get_sentiment(t)
        sent_len = self._get_average_sent_length(t)
        vector = np.hstack((doc_vocab_mat, bigram_counts, trigram_counts, sentiments, sent_len))
        return vector.astype(np.float32), lookup

    def _get_tfidf(self, lines, is_train):
        if is_train:
            doc_vocab_mat = self.tfidf.fit_transform(lines).toarray()
        else:
            doc_vocab_mat = self.tfidf.transform(lines).toarray()
        lookup = {i:v for i, v in enumerate(self.tfidf.get_feature_names())}
        return doc_vocab_mat, lookup

    def _get_average_sent_length(self, t):
        result = np.zeros((len(t),1))
        for i,doc in enumerate(t):
            sents = nltk.sent_tokenize(doc)
            length = 0
            for sent in sents:
                words = nltk.word_tokenize(sent)
                length += len(words)
            sen_len = length/len(sents)
            result[i] = np.clip(sen_len/25, 0,1)
        return result

    def _get_ngram_counts(self, t, n=2):
        tokens = [nltk.word_tokenize(doc) for doc in t]
        flattened = [item for sublist in tokens for item in sublist]
        n_grams = Counter(ngrams(flattened, n)).most_common(NGRAM_SIZE)
        result = np.zeros((len(t), NGRAM_SIZE))
        for i,doc in enumerate(tokens):
            ngram = Counter(ngrams(doc, n))
            for j,key in enumerate(n_grams):
                count = ngram.get(key,0)
                result[i,j]=count
        return result

    def _get_sentiment(self, t):
        sentiments = np.zeros((len(t), len(SENTIMENT_INDEX)))
        for i, doc in enumerate(t):
            tagged = self.stanford_nlp.annotate(doc, properties = SENTIMENT_ANNOTATOR)
            try:
                sentences = json.loads(tagged)[SENTENCES]
                sents = np.zeros(len(SENTIMENT_INDEX))
                for sent in sentences:
                    sentimentValue = int(sent[SENTIMENT_VALUE])
                    sentiment = sent[SENTIMENT]
                    ind = SENTIMENT_INDEX[sentiment]
                    sents[ind] += sentimentValue
                sentiments[i] = sents/len(sentences)
            except Exception as e:
                print(i, tagged)
        return sentiments