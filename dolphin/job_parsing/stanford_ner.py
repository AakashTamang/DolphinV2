from nltk.tokenize import word_tokenize
from nltk.tag.stanford import StanfordNERTagger
import nltk
from datareader import prepare_text
import sys
sys.path.append("..")


class Stanford_NER():
    '''
    Class for applying trained stanford model to our data
    '''

    def __init__(self):
        self.jar_engine_path = "/home/shushant/Desktop/dolphin_repos/DolphinV2/dolphin/job_parsing/stanford-ner.jar"
        self.trained_ner_model_path = "/home/shushant/Desktop/dolphin_repos/DolphinV2/dolphin/job_parsing/final_data_ner_model.ser.gz"

    def parse(self, jd_content):
        '''
        Function for parsing using Stanford Ner

        param jd_content: Textual data of the job description
        return : stanford ner prediction results
        '''
        tokens = word_tokenize(jd_content)
        jar_engine = self.jar_engine_path
        # load trained  ner model
        model = self.trained_ner_model_path
        entity_tagger = StanfordNERTagger(model, jar_engine, encoding="utf8")
        # generate prediction for each and every tokens
        stanford_predictions = entity_tagger.tag(tokens)
        organization = [prediction[0]
                        for prediction in stanford_predictions if prediction[1] == "ORG"]
        location = [prediction[0]
                    for prediction in stanford_predictions if prediction[1] == "LOC"]
        designations = [prediction[0]
                        for prediction in stanford_predictions if prediction[1] == "DESIG"]
        education = [prediction[0]
                     for prediction in stanford_predictions if prediction[1] == "EDU"]
        experience = [prediction[0]
                      for prediction in stanford_predictions if prediction[1] == "EXP"]

        return organization, location, designations, education, experience


if __name__ == "__main__":
    jd_path = "/home/shushant/Desktop/Job Description Collection/QA 17.docx"
    jd_content = prepare_text(jd_path, dolower=False)
    stanford_obj = Stanford_NER()
    organization, location, designations, education, experience = stanford_obj.parse(
        jd_content)
    print("Organizations -->", organization)
    print("Locations --->", location)
    print("Designation ---->", designations)
    print("Education --->", education)
    print("Experience ---> ", experience)
