import logging
import asyncio
import time
import re

import spacy
import pandas as pd
from spacy.tokens import Span, Doc
from spacy.matcher import PhraseMatcher, Matcher
from nltk.tag.stanford import StanfordNERTagger

import settings as cfg
from word2vec import Word2VecScorer
from cvparser.stanfordNER.namedentityrecognition import StanfordNER
from cvparser.segmentation.segmentresume import ResumeSegmentCreator
from cvparser.document_categorization.identify_resume import categorize_document

class NlpPipeline():
    """
     **This class is developed to add the custom spacy pipelines for document categorization, resume segmentation, and resume parsing.**
    """

    def __init__(self):
        """
        **Construcotr method**
        """
        self.logger = logging.getLogger("pipeline_preparation")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s')
        file_handler = logging.FileHandler('pipeline_info.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=['tagger','parser','ner','textcat'])
        except Exception as e:
            # print (e)
            self.logger.exception(e)
        self.ner_tagger = StanfordNERTagger(cfg.NerModelPath,cfg.jarPath,encoding='utf8')
        self.segmentation_obj = ResumeSegmentCreator()
        self.scorer = Word2VecScorer(cfg.word2vec_model)
        try:
            predefined_technical_skills = pd.read_csv(cfg.technical_skills_pool)['Predefined_skills'].to_list()
            predefined_soft_skills = pd.read_csv(cfg.soft_skills_pool)['Predefined_skills'].to_list()
            predefined_languages = pd.read_csv(cfg.languages_pool)['value'].to_list()
            predefined_nationalities = pd.read_csv(cfg.nationality_pool)['Nationality'].to_list()
        except Exception as e:
            # print (e)
            self.logger.exception(e)

        self.soft_skills_pattern = list(self.nlp.pipe(predefined_soft_skills))
        self.technical_skills_patterns = list(self.nlp.pipe(predefined_technical_skills))
        self.languages_pattern = list(self.nlp.pipe(predefined_languages))
        self.nationality_pattern = list(self.nlp.pipe(predefined_nationalities))

    def embedding_component(self,doc):
        '''
        **Gets textual content and returns respective embedding of the document**
        :param: spacy Doc of textual data
        :return: Doc object with embedding
        '''
        doc._.embedding = self.scorer.get_word_embeddings(str(doc))
        # doc2._.embedding = self.scorer.get_word_embeddings(str(doc2))
        return doc

    def category_component(self,doc):
        '''
        **Custom function to add resume identification component to the pipeline**
        params: spacy Doc of textual data
        return : Doc object with category embedded
        '''
        doc._.category = categorize_document(str(doc))
        return doc

    def segmentation_component(self,doc):
        '''
        **Custom function to add resume identification component to the pipeline**
        params: spacy Doc of textual data
        return : Doc object with category embedded
        '''
        resume_segment = self.segmentation_obj.format_segment(str(doc))
        doc._.profile_segment = resume_segment.get('profile')
        doc._.objective_segment = resume_segment.get('objectives')
        doc._.skills_segment = resume_segment.get('skills')
        doc._.academics_segment = resume_segment.get('academics')
        doc._.experience_segment = resume_segment.get('experiences')
        doc._.language_segment = resume_segment.get('languages')
        doc._.projects_segment = resume_segment.get('projects')
        doc._.rewards_segment = resume_segment.get('rewards')
        doc._.references_segment = resume_segment.get('references')
        doc._.links_segment = resume_segment.get('links')
        return doc

    def ner_parsing_component(self,doc):
        '''
        **Function for preparing custom ner parsing component** 
        params: doc of content from file
        return: doc containing parsed information from keyword
        '''
        name,address = StanfordNER.ner_parser(self.ner_tagger,str(doc),"profile")
        education = StanfordNER.ner_parser(self.ner_tagger,str(doc),"academics")
        experiences = StanfordNER.ner_parser(self.ner_tagger,str(doc),"experience")
        doc._.name = name
        doc._.address = address
        doc._.education = education
        doc._.experiences = experiences
        return doc

    def add_ner_parsing(self):
        '''
        **Function for adding custom NER pipeline in nlp model**
        '''
        self.nlp.add_pipe(self.ner_parsing_component,first = True)
        Doc.set_extension('name' , default=None)
        Doc.set_extension('address' , default=None)
        Doc.set_extension("education", default = None)
        Doc.set_extension("experiences", default = None)
        self.logger.info("NER pipeline added")
        

    def pattern_matching_component(self,doc):
        '''
        **Function for preparing pattern matching component in spacy**
        params: doc from document
        return : doc containing matched keywords
        '''        
        # REGEX PATTERN
        phone_patterns = r'([\+\-()\d]{1,8})?\s?([(]?\d{3}[)]?[\s-]?\d{3}[\s-]?\d{3,4})'
        zip_code_patterns = r'(\b\d{5}-\d{4}\b|\b\d{5}\b\s)'
        github_patterns = r'github.com/[^ |^\n]+'
        linkedin_patterns = r"linkedin.com/[^ |^\n]+"

        # SPACY MATCHER
        # phone_patterns = [{"TEXT":{"REGEX":"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$"}}]
        emails_pattern = [{"TEXT": {"REGEX":"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"}}]
        # date_patterns = [{"TEXT":{"REGEX":"\d{4}(?P<sep>[-/])\d{2}(?P=sep)\d{2}"}}]
        date_patterns = [{"IS_DIGIT":True, "LENGTH":{"IN":[2,4]}}, {"TEXT":{"IN":['-']}},{"IS_DIGIT":True, "LENGTH":2,},{"TEXT":{"IN":['-']}},{"IS_DIGIT":True,"LENGTH":{"IN":[2,4]}}]
        gender_patterns = [{"TEXT":{"REGEX":"^(?:m|M|male|Male|f|F|female|Female)$"}}]

        technical_skills_matcher = PhraseMatcher(self.nlp.vocab)
        language_matcher = PhraseMatcher(self.nlp.vocab)
        nationality_matcher = PhraseMatcher(self.nlp.vocab)
        soft_skills_matcher = PhraseMatcher(self.nlp.vocab)

        emails_matcher = Matcher(self.nlp.vocab)
        date_matcher = Matcher(self.nlp.vocab)
        # phone_matcher = Matcher(self.nlp.vocab)
        # emails_matcher = RegexMatcher(self.nlp.vocab)
        # phone_matcher = RegexMatcher(self.nlp.vocab)
        # date_matcher = RegexMatcher(self.nlp.vocab)
        gender_matcher = Matcher(self.nlp.vocab)

        technical_skills_matcher.add("technical_skills",None, *self.technical_skills_patterns)
        soft_skills_matcher.add("soft_skills", None, *self.soft_skills_pattern)
        nationality_matcher.add("nationality",None, *self.nationality_pattern)
        language_matcher.add("languages",None, *self.languages_pattern)

        emails_matcher.add("email",None,emails_pattern)
        date_matcher.add("date",None,date_patterns)
        # phone_matcher.add("phone",None,phone_patterns)
        # emails_matcher.add("emeail",['emails'],kwargs=[{"predef":True}])
        # phone_matcher.add("phone",['phones'],kwargs=[{"predef":True}])
        # date_matcher.add("date",['dates'],kwargs=[{"predef":True}])
        gender_matcher.add("gender",None,gender_patterns)

        technical_skills_matches = technical_skills_matcher(doc)
        soft_skills_matches = soft_skills_matcher(doc)
        nationality_matches = nationality_matcher(doc)
        language_matches = language_matcher(doc)
        emails_matches = emails_matcher(doc)
        # phone_matches = phone_matcher(doc)
        date_matches = date_matcher(doc)
        gender_matches = gender_matcher(doc)
        
        # phone = [Span(doc, start, end, label="phne") for match_id, start, end in phone_matches]
        date = [Span(doc, start, end, label="dates") for match_id, start, end in date_matches]
        gender = [Span(doc, start, end, label="gender") for match_id, start, end in gender_matches]
        emails = [Span(doc, start, end, label="emails") for match_id, start, end in emails_matches]
        
        # If our matcher and regex fails to extract the date or email, this condition will extract them
        if not date or emails:
            if not date:
                nlp2 = spacy.load("en_core_web_sm")
                doc2 = nlp2(doc.text)
                date = [ent.text for ent in doc2.ents if ent.label_ == "DATE"]
            if not emails:
                emails = [token.text for token in doc2 if token.like_email == True]

        technical_skills = [Span(doc, start, end, label="technical_skills") for match_id, start, end in technical_skills_matches]
        soft_skills = [Span(doc, start, end, label="soft_skills") for match_id, start, end in soft_skills_matches]
        nationality = [Span(doc, start, end, label="nationality") for match_id, start, end in nationality_matches]
        language = [Span(doc, start, end, label="languages") for match_id, start, end in language_matches]

        # doc._.phone = set(str(p) for p in phone )
        doc._.phone = set(str(match.group()) for match in re.finditer(phone_patterns,doc.text))
        doc._.date = set(str(d) for d in date )
        doc._.gender = set(str(g) for g in gender )
        doc._.emails = set(str(e) for e in emails )
        doc._.github = set(str(match.group()) for match in re.finditer(github_patterns,doc.text))
        doc._.linkedin = set(str(match.group()) for match in re.finditer(linkedin_patterns,doc.text))
        doc._.zipcode = set(str(match.group()) for match in re.finditer(zip_code_patterns,doc.text))
        
        doc._.nationality = set([str(n) for n in nationality])
        doc._.language = set([str(l) for l in language])
        doc._.technical_skills = set([str(skills) for skills in technical_skills])
        doc._.soft_skills = set([str(skills) for skills in soft_skills])
        return doc

    def add_pattern_matching(self):
        '''
        **Function for adding pattern matching component in pipeline**
        '''
        self.nlp.add_pipe(self.pattern_matching_component)
        Doc.set_extension('technical_skills', default=None, force=True)
        Doc.set_extension('soft_skills', default=None, force=True)
        Doc.set_extension("nationality", default = None, force=True)
        Doc.set_extension("language", default = None, force=True)
        Doc.set_extension("emails", default = None, force=True)
        Doc.set_extension("gender", default = None, force=True)
        Doc.set_extension("date", default = None, force=True)
        Doc.set_extension("phone", default = None, force=True)
        Doc.set_extension("github", default = None, force=True)
        Doc.set_extension("linkedin", default = None, force=True)
        Doc.set_extension("zipcode", default = None, force=True)
        # asyncio.ensure_future(add_ner_parsing())
        self.logger.info("Pattern matching pipeline added")

    def add_embedding_component(self):
        '''
        **Function to add embedding component in pipeline**
        '''
        self.nlp.add_pipe(self.embedding_component)
        Doc.set_extension("embedding", default=None)

    def add_category_component(self):
        """
        **Function to add document categorization component to the spacy custom pipeline**
        """
        self.nlp.add_pipe(self.category_component)
        Doc.set_extension('category', default = None)	

    def add_segmentation_component(self):
        """
        **Function to add resume segmentation component to the spacy custom pipeline**
        """
        self.nlp.add_pipe(self.segmentation_component)
        Doc.set_extension('profile_segment', default = None)
        Doc.set_extension('objective_segment', default = None)
        Doc.set_extension('skills_segment', default = None)
        Doc.set_extension('academics_segment', default = None)
        Doc.set_extension('experience_segment',default = None)
        # Doc.set_extension('academics', default = None)
        Doc.set_extension('language_segment', default = None)
        Doc.set_extension('projects_segment', default = None)
        Doc.set_extension('rewards_segment', default = None)
        Doc.set_extension('references_segment', default = None)
        Doc.set_extension('links_segment', default = None)

    def process_text(self,content):
        """
        **Function to process as spacy doc**
        """
        self.doc = self.nlp(content)
        return self.doc