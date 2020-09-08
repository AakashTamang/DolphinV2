import settings as cfg
from gensim.models import Word2Vec
# from nltk.corpus import stopwords
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

        tokenized = [word_tokenize(token.lower()) for token in token_list]
        flat_list = [item for sublist in tokenized for item in sublist]
        for token in flat_list:
            try:
                doc_word2vec.append(self.word2vec[token])
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
        resume_content = prepare_text(resume_file, dolower=False)
        preprocessed_resume_content = preprocessor_obj.preprocess_text(
            resume_content)
        resume_vector = self.get_word_embeddings(preprocessed_resume_content)
        score = {}
        for jd in job_descriptions:
            job_description = jd['job_description']
            job_text = preprocessor_obj.preprocess_text(job_description)
            job_vector = self.get_word_embeddings(job_text)
            similarity = self.calculate_similarity(job_vector, resume_vector)
            print (similarity)
            score[jd['pk']] = int(similarity*100)
            print (score)
            # for job_id, job_description in jd.items():
            #     job_text = preprocessor_obj.preprocess_text(job_description)
            #     job_vector = self.get_word_embeddings(job_text)
            #     similarity = self.calculate_similarity(job_vector, resume_vector)
            #     score[job_id] = int(similarity * 100)
        return score


if __name__ == "__main__":
    scorer_obj = Word2VecScorer(cfg.word2vec_model)
    test1 = "I want a job in python"
    test2 = "We need a django developer"
    test1_embedding = scorer_obj.get_word_embeddings(test1)
    test2_embedding = scorer_obj.get_word_embeddings(test2)
    similarity = scorer_obj.calculate_similarity(
        test1_embedding, test2_embedding)
