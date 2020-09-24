import re
import string
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
# nltk.download('stopwords')
# NLTK Stop words
from nltk.corpus import stopwords

# Gensim
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_numeric

# spacy for lemmatization
import spacy

# Enable logging for gensim - optional
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)


import warnings
warnings.filterwarnings("ignore",category=DeprecationWarning)

stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could', '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right', 'line', 'even', 'also', 'may', 'take', 'come'])

# df = pd.read_excel("datasets/final_docs_data.xlsx")
df = pd.read_excel("../datasets/raw_train_data.xlsx")
# df = pd.read_excel("datasets/test.xlsx")

# docs_data.info()
# print(docs_data.category.unique())

def sent_to_words(sentences):
    for sent in sentences:
        sent = str(sent)
        sent = re.sub('\S*@\S*\s?', '', sent)  # remove emails
        sent = re.sub("(\s\d+)", "", sent) #remove numbers
        sent = re.sub(r"\b[a-zA-Z]\b", "",sent) #remove single character
        sent = re.sub('\s+', ' ', sent)  # remove newline chars
        sent = re.sub("\'", "", sent)  # remove single quotes
        sent = gensim.utils.simple_preprocess(str(sent), deacc=True) 
        yield(sent)  

# Convert to list
data = df.document.values.tolist()
# pprint(data[0])
# exit()
data_words = list(sent_to_words(data))

# Build the bigram and trigram models
bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = gensim.models.Phrases(bigram[data_words], threshold=100)  
bigram_mod = gensim.models.phrases.Phraser(bigram)
trigram_mod = gensim.models.phrases.Phraser(trigram)

# !python3 -m spacy download en  # run in terminal once
def process_words(texts, stop_words=stop_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """Remove Stopwords, Form Bigrams, Trigrams and Lemmatization"""
    texts = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]
    texts = [bigram_mod[doc] for doc in texts]
    texts = [trigram_mod[bigram_mod[doc]] for doc in texts]
    texts_out = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    # remove stopwords once more after lemmatization
    texts_out = [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts_out]    
    return texts_out

##this data_ready data can also be used as to create feature for a deep learning model
data_ready = process_words(data_words)  # processed Text Data!

df["Text"] = data_ready

writer = pd.ExcelWriter('check_data.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')

# # Close the Pandas Excel writer and output the Excel file.
writer.save()

# # Create Dictionary
# id2word = corpora.Dictionary(data_ready)

# # Create Corpus: Term Document Frequency
# corpus = [id2word.doc2bow(text) for text in data_ready]