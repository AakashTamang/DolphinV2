import spacy
import logging

import settings as cfg
from cvparser.document_categorization.doc_classifier_test import DocClassifier


logger = logging.getLogger("document_category")
logger.setLevel(logging.INFO)


formatter = logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s')


file_handler = logging.FileHandler('document_type_info.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

tfidfModelPath = cfg.tfidf_vec_path
classifierModelPath = cfg.SVC_classifier

nlp = spacy.load("en_core_web_sm", disable=[
                 'ner','parser','textcat']) # disabling tagger won't work for identification


docObj = DocClassifier(tfidfModelPath, classifierModelPath, nlp)

def categorize_document(file_content):
    category = docObj.classify(file_content)
    logger.info("The document is categorized as {}".format(category))
    return category

# new_doc = "Bachelors degree in Computer science"
# result = categorize_document(new_doc)
# print (result)