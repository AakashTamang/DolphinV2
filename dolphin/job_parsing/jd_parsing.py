import sys
sys.path.append("..")
from datareader import prepare_text
import spacy
import nltk
from settings import jd_parse_ner_model
from nltk.tokenize import sent_tokenize



class SpacyNer():
    def __init__(self):
        self.spacy_ner_model_path = jd_parse_ner_model

    def parse(self, jd_content):
        '''
        Function for parsing using Stanford Ner
        params: jar engine path, trained model path, tokens from the file
        return : stanford ner prediction results
        '''
        tokenized_sentences = sent_tokenize(jd_content)
        nlp = spacy.load(self.spacy_ner_model_path)

        all_organizations = []
        all_designations = []
        all_experiences = []
        all_educations = []
        all_locations = []

        for sent in tokenized_sentences:
            doc = nlp(sent)

            organizations = []
            designations = []
            experiences = []
            educations = []
            locations = []

            for ent in doc.ents:
                if ent.label_ == "DESIG":
                    designations.append(ent.text)
                elif ent.label_ == "ORG":
                    organizations.append(ent.text)
                elif ent.label_ == "EXP":
                    experiences.append(ent.text)
                elif ent.label_ == "DEG":
                    educations.append(ent.text)
                elif ent.label_ == "LOC":
                    locations.append(ent.text)
                else:
                    pass

            all_organizations.append(organizations)
            all_designations.append(designations)
            all_experiences.append(experiences)
            all_educations.append(educations)
            all_locations.append(locations)

        # Removing empty lists
        all_organizations = [
            x for x in all_organizations if x]
        all_designations = [x for x in all_designations if x]
        all_experiences = [
            x for x in all_experiences if x]
        all_educations = [
            x for x in all_educations if x]
        all_locations = [
            x for x in all_locations if x]

        return all_designations, all_organizations, all_experiences, all_educations, all_locations


if __name__ == "__main__":
    jd_path = "/home/shushant/Desktop/data_resume/Abinash Bhattarai_QA_Srimatrix.docx"
    jd_content = prepare_text(jd_path, dolower=False)
    spacy_obj = SpacyNer()
    designations, organization, experience, education, location = spacy_obj.parse(
        jd_content)
    print("Organizations -->", organization)
    print("Locations --->", location)
    print("Designation ---->", designations)
    print("Education --->", education)
    print("Experience ---> ", experience)
