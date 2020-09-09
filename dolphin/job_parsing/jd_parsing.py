import sys
# sys.path.append("..")
from datareader import prepare_text
import spacy
import nltk
from settings import jd_parse_ner_model
from nltk.tokenize import sent_tokenize
from cvparser.pipeline import NlpPipeline


class SpacyNer():
    def __init__(self):
        self.spacy_ner_model_path = jd_parse_ner_model
        self.spacy_pipeline = NlpPipeline()
        self.spacy_pipeline.add_skills_pattern_matching()

    def clean_parse_jd(self,file_path):
        cleaned_text = prepare_text(file_path,dolower=False)
        desig, org, exp, edu, loc = self.parse(cleaned_text)
        technical_skills,soft_skills = self.get_skills(cleaned_text)
        result = self.formatted_data(desig, org, exp, edu, loc, technical_skills,soft_skills)
        return result


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
        all_designations = [list({desig.lower() for x in all_designations if x for desig in x})]
        all_experiences = [
            x for x in all_experiences if x]
        all_educations = [
            x for x in all_educations if x]
        all_locations = [
            x for x in all_locations if x]

        return all_designations, all_organizations, all_experiences, all_educations, all_locations

    def get_skills(self,jd_content):
        '''
        This method extracts the technical skills and the soft skills from the given job description document
        :param jd_content: A cleaned text of the job description
        :type jd_content: str
        :return: A set of technical skills and soft skills
        '''
        self.jd_skills = self.spacy_pipeline.process_text(jd_content)
        # print (self.spacy_pipeline.nlp.pipe_names)
        technical_skills = list(self.jd_skills._.technical_skills)
        soft_skills = list(self.jd_skills._.soft_skills)
        return technical_skills,soft_skills

    def formatted_data(self,desig, org, exp, edu, loc,technical_skills,soft_skills):
        json_data = {
            "DESIGNATION": desig,
            "ORGANIZATION": org,
            "EXPERIENCE": exp,
            "EDUCATION": edu,
            "LOCATION": loc,
            "SKILLS":{
                "TECHNICAL_SKILLS": list(technical_skills),
                "SOFT_SKILLS": list(soft_skills),
            }
        }
        return json_data

# if __name__ == "__main__":
#     jd_path = r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\jd_files\backend.txt"
#     jd_content = prepare_text(jd_path, dolower=False)
#     spacy_obj = SpacyNer()
#     designations, organization, experience, education, location = spacy_obj.parse(
#         jd_content)
#     print("Organizations -->", organization)
#     print("Locations --->", location)
#     print("Designation ---->", designations)
#     print("Education --->", education)
#     print("Experience ---> ", experience)
    
#     technical_skills, soft_skills = spacy_obj.get_skills(jd_content)
#     print (f"Technical Skills: {technical_skills}")
#     print (f"Soft Skills: {soft_skills}")