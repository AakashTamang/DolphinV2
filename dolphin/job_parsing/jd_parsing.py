import sys
sys.path.append("..")
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
        Function for parsing usiing custom Spacy NER
        params: job content in text
        return : list of strings of predictions
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
        

        #converting to flat list or list of strings
        organizations = [item for sublist in all_organizations for item in sublist]
        designations = [item for sublist in all_designations for item in sublist]
        educations = [item for sublist in all_educations for item in sublist]
        experiences = [item for sublist in all_experiences for item in sublist]
        locations = [item for sublist in all_locations for item in sublist]

        #Removing if the predictions from spacy model are more than 50 characters
        final_organizations = [item for item in organizations if len(item)<=50]
        final_experiences = [item for item in experiences if len(item)<=50]
        final_educations = [item for item in educations if len(item)<=50]
        final_locations = [item for item in locations if len(item)<=50]
        final_designations = [item for item in designations if len(item)<=50]
        # ---Always return list of strings from here----
        return final_designations, final_organizations, final_educations, final_experiences, final_locations

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

if __name__ == "__main__":
    # jd_path = r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\jd_files\backend.txt")
    # jd_content = prepare_text(jd_path, dolower=False)
    # jd_content = "Qualifications Experience:US citizenship, 1 year (Required) Education : Bachelor's (Required) Work authorization : United States (Required) Full Job Description DOD client (US Citizenship required) Position Summary You will be a software engineer tasked with developing, testing and maintaining a suite of software applications and tools that support our aircraft survivability programs. Your role will require operating as a member of an integrated team alongside other engineering disciplines such as embedded software, systems engineering and product/test engineering. Basic Qualifications and Required Skills B.S. in Computer Science, Computer Engineering, Software Engineering or a related disciplne from an accredited institution or equivalent combination of education and experience.5+ years of experience in software engineering. Active security clearance or ability to obtain security clearance is required Expertise in Python Expertise in object oriented software development Experience developing desktop applications with the .NET Framework, C#, Visual Studio Experience developing desktop applications and/or software libraries with C or C++ is nice to haveExperience with source control repositories such as Git or SVNExperience following an established software engineering processExperience with software build tools such as JenkinsExcellent written and verbal communication skills required Duties and Responsibilities Responsible for software engineering tasks including requirements/user story definition, software application and library design, implementation, integration, verification, validation and maintenance. Other duties as assigned.Job Type: ContractPay: $50.00 - $70.00 per hour Benefits: Dental insurance Health insurance Schedule: Monday to Friday COVID-19 considerations:Due to the nature of the work, candidates must be available to work onsite in a secure area. Experience : US citizenship: 1 year (Required) Education :Bachelor's (Required) Work authorization: United States (Required) Contract Renewal: Likely Full Time Opportunity : YesCompany's website:www.cornerstonetek.com Work Remotely:Temporarily due to COVID-19 If you require alternative methods of application or screening, you must approach the employer directly to request this as Indeed is not responsible for the employer's application process.\n"
    # spacy_obj = SpacyNer()
    # designations, organization, experience, education, location = spacy_obj.parse(
    #     jd_content)
    # print("Organizations -->", organization)
    # print("Locations --->", location)
    # print("Designation ---->", designations)
    # print("Education --->", education)
    # print("Experience ---> ", experience)
    
    # technical_skills, soft_skills = spacy_obj.get_skills(jd_content)
    # print (f"Technical Skills: {technical_skills}")
    # print (f"Soft Skills: {soft_skills}")