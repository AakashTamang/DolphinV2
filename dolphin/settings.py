import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
tempStorage = os.path.join(ROOT,'tempStorage')


'''<------------Directory Absolute Paths------------------------------>'''
RootDir = os.path.dirname(os.path.abspath(__file__))
ParserDir = os.path.join(RootDir,'cvparser')
ScorerDir = os.path.join(RootDir,'cvscorer')
CommonDir = os.path.join(RootDir,'common')

'''<----------NER Model Files --------->'''
jarPath = os.path.join(CommonDir,'stanfordNER/stanford-ner.jar')
NerModelPath = os.path.join(CommonDir,'stanfordNER/NER_model.ser.gz')

'''<--------- Document Classification Model------>'''
tfidf_vec_path = os.path.join(ParserDir, 'models/tfidf1.pkl')
SVC_classifier = os.path.join(ParserDir,"models/new_model_svc.pkl")

'''<-----Segementation Model ---->'''
ResumeSegmentationModelPath = os.path.join(ParserDir,'models/segment_identifier.pkl')

'''<-----Custom Word2vec model --->'''
word2vec_model = os.path.join(ScorerDir, "models/word2vec_model")

'''<-------Pool Parser files--------->'''
technical_skills_pool = os.path.join(ParserDir,'data/technical_skills.csv')
soft_skills_pool = os.path.join(ParserDir,'data/soft_skills_resume.csv')
languages_pool = os.path.join(ParserDir,'data/languages.csv')
nationality_pool = os.path.join(ParserDir,'data/nationality_data.csv')

"<---------------------Write to file ----------------------------------->"
Write2file = True

'''<-------Job Parsig NER model--------->'''
jd_parse_ner_model = os.path.join(RootDir,'job_parsing/JobParsingSpacyNERFinal')
