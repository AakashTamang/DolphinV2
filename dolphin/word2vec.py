import settings as cfg
from gensim.models import Word2Vec
# from nltk.corpus import stopwords
import ast
from nltk.tokenize import word_tokenize
from scipy import spatial
import numpy as np
import nltk
import string
from datareader import prepare_text
from data_preprocessing import PreprocessData
# from job_parsing.jd_parsing import SpacyNer
# from settings import technical_skills_pool, soft_skills_pool
# from cvparser.pipeline import NlpPipeline


# nltk.download('stopwords')

# stop_words = set(stopwords.words('english'))

preprocessor_obj = PreprocessData()

# NerObj = SpacyNer()
# spacy_pipeline = NlpPipeline()
# spacy_pipeline.add_skills_pattern_matching()


class Word2VecScorer():
    '''
    Gives embeddings similarity between two textual contents
    '''

    def __init__(self, word2vec_path):
        """
        This cosntructor loads the word2vec model that will be used for getting the  word embeddings on the textual document and give similarity between two documents
        """
        self.word2vec = Word2Vec.load(word2vec_path)

    def get_word_embeddings(self, token_list):
        '''
        Takes the list of the tokenized
        resumes and returns their embedded vectors
        :param resume_token_list:type list of list
        :return:cv_word2vec :type list of list
        '''
        doc_word2vec = list()
        if type(token_list) == str:
            token_list = token_list.lower()
            flat_list = word_tokenize(token_list)
        else:
            token_list = token_list[0].lower()
            flat_list = word_tokenize(token_list)
        
        # print("Flat list is this -- {}  type --{}".format(flat_list,type(flat_list)))
        for token in flat_list:
            try:
                doc_word2vec.append(self.word2vec[token])
                # print("Now Token",token)
            except KeyError as K:
                # logger.exception(msg=K)
                print("Keyerror here....:  ", K)

        doc_vectors = (np.mean(doc_word2vec, axis=0))
        return doc_vectors

    def calculate_similarity(self, first_vector, second_vector):
        """
        This function makes the use of cosine distance to measure the similarity between two embeddings
        :param: first_vector
        :type:list
        :param:second_vector
        :type:list
        :return: similarity
        :rtype: float
        """
        similarity = (
            (1 - spatial.distance.cosine(first_vector, second_vector)))
        if similarity < 0:
            similarity = 0
        elif similarity > 100:
            similarity = 100
        return similarity

    def calculate_score(self, resume_file, job_descriptions):
        '''
        Calculates similarity score between resume and job-description
        :params: resume_file :type:str
                 job_descriptions :type:list
        :returns: score :type:dict
        '''
        resume_content = prepare_text(resume_file, dolower=False)
        preprocessed_resume_content = preprocessor_obj.preprocess_text(
            resume_content)
        preprocessed_resume_content = " ".join(preprocessed_resume_content)
        # res_technical_skills, res_soft_skills = NerObj.get_skills(preprocessed_resume_content)
        # jd_skills = spacy_pipeline.process_text(preprocessed_resume_content)
        # res_technical_skills = jd_skills._.technical_skills
        # res_soft_skills = jd_skills._.soft_skills

        # preprocessed_resume_content = resume_content
        resume_vector = self.get_word_embeddings(preprocessed_resume_content)
        score = {}
        for jd in job_descriptions:
            if type(jd) == str:
                jd = ast.literal_eval(jd)
            else:
                pass
            job_description = jd['job_description']
            job_text = preprocessor_obj.preprocess_text(job_description)
            job_text = " ".join(job_text)
            # jd_technical_skills, jd_soft_skills = NerObj.get_skills(job_text)
            # jd_skills = spacy_pipeline.process_text(job_text)
            # jd_technical_skills = jd_skills._.technical_skills
            # jd_soft_skills = jd_skills._.soft_skills
            # matched_soft_skills = res_soft_skills.intersection(jd_soft_skills)
            # matched_technical_skills = res_technical_skills.intersection(jd_technical_skills)

            # if matched_technical_skills != 0:
            #     try:
            #         technical_skill_score = len(matched_technical_skills) / len(jd_technical_skills) * 35
            #     except:
            #         technical_skill_score = 35
            # else:
            #     technical_skill_score = 0
            
            # if matched_soft_skills != 0:
            #     try:
            #         soft_skills_score = len(matched_soft_skills) / len(jd_soft_skills) * 5
            #     except:
            #         soft_skills_score = 5
            # else:
            #     soft_skills_score = 0
            
            # skill_score = technical_skill_score + soft_skills_score

            # job_text = job_description
            job_vector = self.get_word_embeddings(job_text)
            similarity = self.calculate_similarity(job_vector, resume_vector)
            if np.isnan(similarity):
                similarity = 0
            word2vecscore = int(similarity*100)
            # score[jd['pk']] = word2vecscore + skill_score
            score[jd['pk']] = word2vecscore
            # print(score)
        return score

    def score_jobs(self, job_1,job_1_title,other_jobs):
        '''
        Calculates score between multiple jobs
        :params: job_1 :type:str
                 job_1_title :type:str
                 other_jobs :type:list
        :returns: sorted_job_score :type:list of scores
        '''
        preprocessed_job_1 = preprocessor_obj.preprocess_text(job_1)
        preprocessed_job_1_formatted = " ".join(preprocessed_job_1)
        job_vector_1 = self.get_word_embeddings(preprocessed_job_1_formatted)
        job_title_1 = job_1_title
        job_score = {}
        for job in other_jobs:
            job_text = job['job_description']
            job_title = job['job_title']
            job_text_preprocessed = preprocessor_obj.preprocess_text(job_text)
            job_text_preprocessed_formatted= ' '.join(job_text_preprocessed)
            print("Other job ",job_text_preprocessed_formatted)
            print("The job",preprocessed_job_1_formatted)
            job_text_vector = self.get_word_embeddings(job_text_preprocessed_formatted)
            simialrity = self.calculate_similarity(
                job_vector_1, job_text_vector)
            if job_title.lower() == job_title_1.lower():
                desig_score = 20
            else:
                desig_score = 0
            content_score = int(simialrity * 80)
            job_score[job['pk']] = desig_score + content_score
            print("Desig score ---{} Content score -- {}".format(desig_score,content_score))
        
        sorted_job_score = {k: v for k, v in sorted(job_score.items(), key=lambda item: item[1],reverse = True)}
        # top_four_job_score = {k: sorted_job_score[k] for k in list(sorted_job_score)[:4]}
        return sorted_job_score


# if __name__ == "__main__":
#     scorer_obj = Word2VecScorer(cfg.word2vec_model)
#     test1 = "I want a job in python"
#     test2 = "We need a django developer"
#     test1_embedding = scorer_obj.get_word_embeddings(test1)
#     test2_embedding = scorer_obj.get_word_embeddings(test2)
#     similarity = scorer_obj.calculate_similarity(
#         test1_embedding, test2_embedding)
