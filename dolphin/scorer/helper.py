import nltk
import spacy
import textacy
import pandas as pd
from nltk.tag import pos_tag
from nltk import RegexpParser
from nltk.corpus import stopwords

class PreprocessData:

    def __init__(self,spacy_corpus='en_core_web_sm',n_gram_len=3):
        self.n_gram_len = n_gram_len
        self.nlp = spacy.load(spacy_corpus)
        self.stopwords = set(stopwords.words('english'))
        self.priority_tag = {'NN','NNP','NNS','VB','CD'}
        self.tagged_tokens = []
        self.tokenized_text = []
        self.doc = []
        self.ngrams = None

    def preprocess_text(self, text,filter_tag = True):
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
            final_tokens = [word for word, pos in self.tagged_tokens \
                            if pos in self.priority_tag]
            final_tokens = [word for word in final_tokens\
                            if word not in self.stopwords]
        else:
            final_tokens = [word for word,pos in self.tagged_tokens]
        return final_tokens


class NLTKHelper:

    def __init__(self,chunk_rules):
        self.chunk_rules = chunk_rules


    def experiencefinder(self,tagged_tokens):
        '''
        Takes the tokenized job description section of the
        posted job and uses the nltk regex chunker to chunk the
        experience out from the section
        :param description_section :type str
        :return:provides the list of experience chunked
        '''
        chunked_phrases = []
        for rule in self.chunk_rules:
            chunk_parser = RegexpParser(rule)
            matched_phrases = chunk_parser.parse(tagged_tokens)
            for subtree in matched_phrases:
                if type(subtree) == nltk.Tree and subtree.label() == rule.partition(':')[0]:
                    chunked_phrases.append(" ".join([token for token, pos in subtree.leaves()]))
        return (chunked_phrases)


    def skillsfinder(self,n_grams,skillFilePath):
        '''
        Takes the n-grams created from any document
        then compares them to the existing pool of
        the skills
        :param n_grams    :type list
        :return: provides the set of skills found
        '''

        skills = pd.read_csv(skillFilePath)
        skill_mapper = {skill.lower():skill for skill in n_grams}
        total_skills = [skill.lower() for skill in n_grams]
        skills['matched'] = skills['Predefined_skills'].apply(lambda x: 1 if x.lower() in total_skills else 0)
        matched_skills = skills.Predefined_skills.loc[skills['matched'] == 1].values
        matched_skills = matched_skills.tolist()
        formatted_skills = {skill_mapper.get(skill) for skill in matched_skills}
        return formatted_skills