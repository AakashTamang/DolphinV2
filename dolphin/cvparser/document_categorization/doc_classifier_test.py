import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import pickle
# Gensim
from gensim.utils import simple_preprocess
from gensim.models import Phrases
from gensim.models.phrases import Phraser

class DocClassifier:
    def __init__(self, tfidfmodelpath, classifiermodelpath, nlp):
        # self.processed_text = processed_text
        self.tfidfmodelpath = tfidfmodelpath
        self.classifiermodelpath = classifiermodelpath
        self.nlp = nlp

    def sent_to_words(self,file_content):
        for sent in [file_content]:
            sent = re.sub('\S*@\S*\s?', '', sent)  # remove emails
            sent = simple_preprocess(str(sent), deacc=True)
            yield(sent)  

        # !python3 -m spacy download en  # run in terminal once
    def preprocess_words(self,texts, stop_words, bigram_mod, trigram_mod, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
        texts = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
        texts = [bigram_mod[doc] for doc in texts]
        texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
        texts_out = []
        for sent in texts:
            doc = self.nlp(" ".join(sent)) 
            texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
        # remove stopwords once more after lemmatization
        texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]    
        return texts_out

    def classify(self,file_content):
        stop_words = stopwords.words('english')
        stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])
        
        #To test model from pdf files
        data_words = list(self.sent_to_words(file_content))
        # Build the bigram and trigram models
        bigram = Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
        trigram = Phrases(bigram[data_words], threshold=100)  
        bigram_mod = Phraser(bigram)
        trigram_mod = Phraser(trigram)

        ##this data_ready data can also be used as to create feature for a deep learning model
        data_ready = self.preprocess_words(data_words,stop_words, bigram_mod,trigram_mod)  # processed Text Data!
        data_ready = [item for sublist in data_ready for item in sublist]
        data = " ".join(data_ready)
        #load vocabulary from the vectorizer
        tf1 = pickle.load(open(self.tfidfmodelpath, 'rb'))
        vectorizer = TfidfVectorizer(vocabulary=tf1.vocabulary_)

        # Load from file
        with open(self.classifiermodelpath, 'rb') as file:
            pickle_model = pickle.load(file)

        X = vectorizer.fit_transform([data])
        result = pickle_model.predict(X).tolist()
        result_map = {1:"resume",0:"others",2:"job_description"}
        category = result_map.get(result[0])
        return category