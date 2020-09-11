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

# nltk.download('stopwords')

# stop_words = set(stopwords.words('english'))

preprocessor_obj = PreprocessData()


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
            # print("Samasyaaa yaha xa {} ani type {}".format(token_list,type(token_list)))
            token_list = token_list[0][0].lower()
            flat_list = word_tokenize(token_list)
            # tokenized = [word_tokenize(token.lower()) for token in token_list]
            # flat_list = [item for sublist in tokenized for item in sublist]
        # print("Flat list vanya yehi ho la boro {}".format(flat_list))
        for token in flat_list:
            try:
                doc_word2vec.append(self.word2vec[token])
            except KeyError as K:
                # logger.exception(msg=K)
                # print("Keyerror here....:  ", K)
                pass

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
        resume_content = prepare_text(resume_file, dolower=False)
        preprocessed_resume_content = preprocessor_obj.preprocess_text(
            resume_content)
        preprocessed_resume_content = " ".join(preprocessed_resume_content)
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
            job_vector = self.get_word_embeddings(job_text)
            similarity = self.calculate_similarity(job_vector, resume_vector)
            if np.isnan(similarity):
                similarity = 0
            score[jd['pk']] = int(similarity*100) + 20
            # print(score)
        return score

    def score_jobs(self, job_1, other_jobs):
        preprocessed_job_1 = preprocessor_obj.preprocess_text(job_1)
        job_vector_1 = self.get_word_embeddings(preprocessed_job_1)
        job_score = {}
        import pdb;pdb.set_trace()
        for job in other_jobs:
            job_text = job['job_description']
            job_text_preprocessed = preprocessor_obj.preprocess_text(job_text)
            job_text_vector = self.get_word_embeddings(job_text_preprocessed)
            simialrity = self.calculate_similarity(
                job_vector_1, job_text_vector)
            job_score[job['pk']] = int(simialrity * 100)
        return job_score


# if __name__ == "__main__":
#     scorer_obj = Word2VecScorer(cfg.word2vec_model)
#     test1 = "I want a job in python"
#     test2 = "We need a django developer"
#     test1_embedding = scorer_obj.get_word_embeddings(test1)
#     test2_embedding = scorer_obj.get_word_embeddings(test2)
#     similarity = scorer_obj.calculate_similarity(
#         test1_embedding, test2_embedding)
