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
        '''
        pos_tags:
        NN - noun, singular eg: - ‘desk’
        NNS - noun, plural eg: - ‘desks’
        NNP - proper noun, singular eg: - ‘Harrison’
        VB - verb, base form eg: - take is the base form of taking
        CD - Cardinal digit
        '''
        self.n_gram_len = n_gram_len
        self.nlp = spacy.load(spacy_corpus)
        load_stopwords = set(stopwords.words('english'))
        new_stop_words = ['developer','skills','requirement','qualification','education','good','experienced','engineer','technology','stakeholders','potential','may', 'usedwpf', 'patient','florida', 'techniques', '6', 'filters','template', 'themes', 'atlanta', 'project','data',
        'help','research','domain','results','ingest','transformation','transfer','opportunities','training','customers','knowledge','etc','experience','technical','computer', 'dependency', 'achieve', 'panel', 'phases', 'performance','extender', 'sources', 'solid', 'order',
        'non-technical','contenterra', 'consumed', 'basis', 'reviews', 'script','cycle', 'pages', 'andhra','architecture', 'implementation', 'solutions', 'crystal','generate', 'reston', 'specification', 'support', 'mapping', 'queries', 'designs', 'generator', 'systems', 'department',
        'staff', 'iis', 'commit', 'feel', 'inc.', 'life', 'distributed', 'board','sign-on', 'rates', 'writing','databases', 'applicationsleveragingado.net','schemas', 'service', 'connectivity', 'meetings', 'base', 'directives','change', 'relational', 'crated', 'website', 'utilize',
        'accept', 'controller', 'workflows','hands', 'section', 'tortoise', 'intelligence','pharmacy', 'skins', 'forms', 'look', 'dec', 'functions', 'action', 'test', 'services', 'file','client','clients','process','responsible', 'site', 'versions', 'installation', 'reusability', 'work',
        'reader', 'map', 'source', 'industry', 'react', 'configurations','iterative','succeed', 'ability','program', 'features', 'conflict','applications','application','need','require','execution','budets','retrieve','ado','done','improve','end','complete','block','purchase',
        'transactions', 'controls', 'get','single','create','issues','safe','phone','number','country','city','state','place','advantage','able','familirity','volunteers','tech','custom','bay','follow','focus','revit','responsibility','responsibilities','want','meet','write','travel',
        'document','way','provide','growth','execute']
        self.stopwords = load_stopwords.union(new_stop_words)
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
            final_tokens = [word.lower() for word, pos in self.tagged_tokens
                            if pos in self.priority_tag]
            final_tokens = [word for word in final_tokens
                            if word not in self.stopwords]
        else:
            final_tokens = [word for word, pos in self.tagged_tokens]

        final_tokens = list({tok for tok in final_tokens})
        # print (f"final_tokens: \n{final_tokens}")
        # print ("\n---------------------------------\n")
        return final_tokens
