import unittest

from nltk.tag.stanford import StanfordNERTagger


from dolphin.settings import NerModelPath,jarPath
from dolphin.datareader import prepare_text
from dolphin.stanfordNER.namedentityrecognition import StanfordNER

ner_tagger = StanfordNERTagger(NerModelPath,jarPath,encoding = 'utf8')


class TestNER(unittest.TestCase):
    def test_profile_parsing(self):
        '''
        Function for testing wheather personal profile is being parsed from NER model or not
        '''
        resume_content = prepare_text("/home/shushant/Desktop/data_resume/Aakriti_QA.docx")
        name,address = StanfordNER.ner_parser(ner_tagger,resume_content,"profile")
        self.assertIsNotNone(name)
        self.assertIsNotNone(address)
    
    def test_academics_parsing(self):
        '''
        Function for testing education is being parsed from the resume using the NER model or not
        '''
        resume_content = prepare_text("/home/shushant/Desktop/data_resume/Aakriti_QA.docx")
        academics = StanfordNER.ner_parser(ner_tagger,resume_content,"academics")
        self.assertIsNotNone(academics)
    
    def test_experience_parsing(self):
        '''
        Function for testing wheather experience is being parsed from resume using NER model or not
        '''
        resume_content = prepare_text("/home/shushant/Desktop/data_resume/Aakriti_QA.docx")
        experiences = StanfordNER.ner_parser(ner_tagger,resume_content,"experience")
        self.assertIsNotNone(experiences)

if __name__ ==  "__main__":
    unittest.main()
