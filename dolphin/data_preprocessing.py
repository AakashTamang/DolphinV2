import nltk
import spacy
import textacy
import pandas as pd
from nltk.tag import pos_tag
from nltk import RegexpParser
from nltk.corpus import stopwords


class PreprocessData:
    """
    Class for preprocessing contents from resumes or job descriptions
    """

    def __init__(self, spacy_corpus='en_core_web_sm', n_gram_len=3):
        self.n_gram_len = n_gram_len
        self.nlp = spacy.load(spacy_corpus)
        self.stopwords = set(stopwords.words('english'))
        self.priority_tag = {'NN', 'NNP', 'NNS', 'VB', 'CD'}
        self.tagged_tokens = []
        self.tokenized_text = []
        self.doc = []
        self.ngrams = None

    def preprocess_text(self, text, filter_tag=True):
        '''
        Preprocessing function that takes the plain text
        removes words other than nouns and verbs then
        removes the stop words if any in the filtered_tokens
        :param text:type str
        :return:final_tokens :type list
        '''
        self.doc = self.nlp(text)
        # self.tokenized_text_test = [token.text for token in self.doc]
        self.tokenized_text = nltk.word_tokenize(text)
        self.tagged_tokens = pos_tag(self.tokenized_text)
        n_gram_words = set()
        for i in range(self.n_gram_len):
            n_gram_words.update(set(textacy.extract.ngrams(self.doc, i+1)))
        self.n_grams = {ngm.text for ngm in n_gram_words}
        if filter_tag == True:
            final_tokens = [word for word, pos in self.tagged_tokens
                            if pos in self.priority_tag]
            final_tokens = [word for word in final_tokens
                            if word not in self.stopwords]
        else:
            final_tokens = [word for word, pos in self.tagged_tokens]

        final_tokens = list({tok.lower() for tok in final_tokens})
        return final_tokens
