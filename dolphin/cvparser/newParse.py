import time
import glob
import cProfile, pstats, io
import os
import re

from datareader import prepare_text
from cvparser.stanfordNER import formatdata
from cvparser.pipeline import NlpPipeline
from word2vec import Word2VecScorer
import settings as cfg

# java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
# os.environ['JAVAHOME'] = java_path

class Parser:
    
    def __init__(self):
        '''
        Initializer that creates an object of the spaCy and adds all the 5 pipeline components.
        It will also take the path of the resume
        '''
        self.spacy_pipeline = NlpPipeline()
        self.spacy_pipeline.add_category_component()
        self.spacy_pipeline.add_segmentation_component()
        # self.spacy_pipeline.add_ner_parsing()
        self.spacy_pipeline.add_profile_ner_parsing()
        # self.spacy_pipeline.add_academics_ner_parsing()
        # self.spacy_pipeline.add_experience_ner_parsing()
        self.spacy_pipeline.add_experience_academics_ner_parsing_component()
        # self.spacy_pipeline.add_pattern_matching()
        self.spacy_pipeline.add_profile_pattern_matching()
        self.spacy_pipeline.add_skills_pattern_matching()
        self.spacy_pipeline.add_embedding_component()

    def identifyResume(self,resume_path):
        '''
        This method will identify if a given document is a resume or job description or others.
        Except the "category_component" pipeline, all the other pipeline components are disabled

        :param resume_path: Takes the path of the resume
        :return: Executes the respective method as per document is classified
        '''
        self.cleaned_resume = prepare_text(resume_path,dolower=False)
        # with self.spacy_pipeline.nlp.disable_pipes("segmentation_component","profile_ner_parsing_component","academics_ner_parsing_component","experience_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
        with self.spacy_pipeline.nlp.disable_pipes("segmentation_component","profile_ner_parsing_component","experience_academics_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
            self.classify_doc = self.spacy_pipeline.process_text(self.cleaned_resume)
        document_classified = {
            'resume': self.parseCV,
            'job_description': self.rejectCV,
            'others': self.rejectCV,
        }
        return document_classified[self.classify_doc._.category]()

    def parseCV(self):
        '''
        This method will be executed if a given document is identified as a resume.
        The resume will be passed to the spaCy pipeline for processing.
        Here, the "segmentation_component" pipeline is enabled and the others are disabled.

        :return: A structured data in the required JSON format
        '''
        # with self.spacy_pipeline.nlp.disable_pipes("category_component","profile_ner_parsing_component","academics_ner_parsing_component","experience_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
        with self.spacy_pipeline.nlp.disable_pipes("category_component","profile_ner_parsing_component","experience_academics_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
            self.segmented_resume = self.spacy_pipeline.process_text(self.cleaned_resume)
        final_data = self.getStructuredData()
        return final_data

    # def personal_information_parser(self, profile_segment):
    #     '''
    #     This method will extract the available personal information for the profile segment or the whole resume.
    #     Here, only "ner_parsing_component" and "pattern_matching_component" are enabled.

    #     :param profile_segment: The profile segment from a resume
    #     :type profile_segment: str
    #     :return: Required information from the profile
    #     '''
    #     profile_text = profile_segment
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","embedding_component"):
    #         if profile_text:
    #             self.resume_profile = self.spacy_pipeline.process_text(profile_text)
    #             name,address = self.resume_profile._.name, self.resume_profile._.address
    #             emails = self.resume_profile._.emails
    #             phone = self.resume_profile._.phone
    #             birthdate = self.resume_profile._.date
    #             gender = self.resume_profile._.gender
    #             nationality = self.resume_profile._.nationality
    #             github = self.resume_profile._.github
    #             linkedin = self.resume_profile._.linkedin
    #             zipcode = self.resume_profile._.zipcode
    #         else:
    #             self.resume_profile = self.spacy_pipeline.process_text(self.cleaned_resume)
    #             name,address = self.resume_profile._.name, self.resume_profile._.address
    #             emails = self.resume_profile._.emails
    #             phone = self.resume_profile._.phone
    #             birthdate = self.resume_profile._.date
    #             gender = self.resume_profile._.gender
    #             nationality = self.resume_profile._.nationality
    #             github = self.resume_profile._.github
    #             linkedin = self.resume_profile._.linkedin
    #             zipcode = self.resume_profile._.zipcode
    #     return name,address,list(emails),list(phone),list(zipcode),list(nationality),list(github),list(linkedin),list(birthdate),list(gender)

    def profile_information_parser(self,profile_segment):
        '''
        This method will extract the available personal information for the profile segment or the whole resume.
        Here, only "profile_ner_parsing_component" and "profile_pattern_matching_component" are enabled.

        :param profile_segment: The profile segment from a resume
        :type profile_segment: str
        :return: Required informations from the profile
        '''
        # with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","academics_ner_parsing_component","experience_ner_parsing_component","skills_pattern_matching_component","embedding_component"):
        with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","experience_academics_ner_parsing_component","skills_pattern_matching_component","embedding_component"):
            if profile_segment:
                # self.resume_profile = self.spacy_pipeline.process_text(profile_segment)
                self.resume_profile = self.spacy_pipeline.process_text("".join([profile_segment,self.segmented_resume._.language_segment]))
            else:
                self.resume_profile = self.spacy_pipeline.process_text(self.cleaned_resume)
        name,address = self.resume_profile._.name, self.segmented_resume._.address
        emails = self.resume_profile._.emails
        phone = self.resume_profile._.phone
        phone = [re.sub(r'\s+','',i) for i in phone]
        birthdate = self.resume_profile._.date
        gender = self.resume_profile._.gender
        nationality = self.resume_profile._.nationality
        github = self.resume_profile._.github
        linkedin = self.resume_profile._.linkedin
        zipcode = self.resume_profile._.zipcode
        return name,address,list(emails),list(phone),list(zipcode),list(nationality),list(github),list(linkedin),list(birthdate),list(gender)
    
    # def education_information_parser(self,academics_segment):
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","experience_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
    #             if academics_segment:
    #                 self.resume_education = self.spacy_pipeline.process_text(academics_segment)
    #             else:
    #                 self.resume_education = self.spacy_pipeline.process_text(self.cleaned_resume)

    # def experience_information_parser(self,experience_segment):
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","academics_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
    #         if experience_segment:
    #             self.resume_experience = self.spacy_pipeline.process_text(experience_segment)
    #         else:
    #             self.resume_experience = self.spacy_pipeline.process_text(self.cleaned_resume)

    def experience_academics_parser(self,experience_academics_segment):
        '''
        This method will extract the available experience and academics from the resume.
        Here, only "experience_academics_ner_parsing_component" is enabled.

        :param experience_academics_segment: The experience and education segment from a resume. Here we are using the whole resume. So that we do not miss any experiences.
        :type experience_academics_segment: str
        '''
        with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component","embedding_component"):
            self.resume_experience_academics = self.spacy_pipeline.process_text(experience_academics_segment)

    def skills_language_parser(self):
        '''
        This method will extract the available skills from the resume.
        Here, only "skills_pattern_matching_component" is enabled.
        As the skills can be in many parts of resume, we have passed the whole resume so that we can extract all the possible skills.
        '''
        # with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","academics_ner_parsing_component","experience_ner_parsing_component","profile_pattern_matching_component","embedding_component"):
        with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","experience_academics_ner_parsing_component","profile_pattern_matching_component","embedding_component"):
            self.resume_skills_language = self.spacy_pipeline.process_text(self.cleaned_resume)

    # def skills_parser(self,skill_segment):
    #     '''
    #     This method will extract the technical skills and the soft skills from the skills segment or the whole resume.
    #     Here, only "pattern_matching_component" is enabled.

    #     :param skill_segment: The skill segment from a resume
    #     :type skill_segment: str
    #     :return: A set of technical skills and soft skills
    #     '''
    #     skill_text = skill_segment
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","ner_parsing_component","embedding_component"):
    #         if skill_text:
    #             self.resume_skills = self.spacy_pipeline.process_text(skill_text)
    #             technical_skills = self.resume_skills._.technical_skills
    #             soft_skills = self.resume_skills._.soft_skills
    #         else:
    #             self.resume_skills = self.spacy_pipeline.process_text(self.cleaned_resume)
    #             technical_skills = self.resume_skills._.technical_skills
    #             soft_skills = self.resume_skills._.soft_skills
    #     return list(technical_skills),list(soft_skills)


    # def education_parser(self,edu_segment):
    #     '''
    #     This method will extract the education information from the education segment or from the whole resume.
    #     Here, only "ner_parsing_component" is enabled.

    #     :param edu_segment: The education segment from a resume
    #     :type edu_segment: str
    #     :return: A list of academics degree from a resume
    #     '''
    #     education_text = edu_segment
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","pattern_matching_component","embedding_component"):
    #         if education_text:
    #             self.resume_education = self.spacy_pipeline.process_text(education_text)
    #             academics = self.resume_education._.education
    #         else:
    #             self.resume_education = self.spacy_pipeline.process_text(self.cleaned_resume)
    #             academics = self.resume_education._.education
    #     return academics

    
    # def experience_parser(self,exp_segment):
    #     '''
    #     This method will extract the experiences from the experience segment or from the whole resume.
    #     Here, only "ner_parsing_component" is enabled.

    #     :param exp_segment: The experience segment from a resume
    #     :type exp_segment: str
    #     :return: A list of experiences from a resume
    #     '''
    #     experience_text = exp_segment
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","pattern_matching_component","embedding_component"):
    #         if experience_text:
    #             self.resume_experience = self.spacy_pipeline.process_text(experience_text)
    #             experience = self.resume_experience._.experiences
    #         else:
    #             self.resume_experience = self.spacy_pipeline.process_text(self.cleaned_resume)
    #             experience = self.resume_experience._.experiences
    #     return experience

    # def language_parser(self,lang_segment):
    #     '''
    #     This method will extract the language language segment or from the whole resume.
    #     Here, only "pattern_matching_component" is enabled.

    #     :param lang_segment: The language segment from a resume
    #     :type lang_segment: str
    #     :return: A list of languages from a resume
    #     '''
    #     language_text = lang_segment
    #     with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","ner_parsing_component","embedding_component"):
    #         if language_text:
    #             self.resume_language = self.spacy_pipeline.process_text(language_text)
    #             language = self.resume_language._.language
    #         else:
    #             self.resume_language = self.spacy_pipeline.process_text(self.cleaned_resume)
    #             language = self.resume_language._.language
    #     return list(language)
    

    def returnjson(self,personal_information):
        '''
        This method will arrange all the informations in the required JSON format.
        
        :param personal_information: Personal information of a resume
        :type personal_information: tuple
        :return: All required information in the JSON format
        '''
        personalInfo = formatdata.formatPersonalinfo(personal_information)
        # json_data = {
        #     "PERSONAL_INFORMATION": personalInfo,
        #     "OBJECTIVE": self.segmented_resume._.objective_segment,
        #     "SKILLS":{
        #         'Skills': list(self.resume_skills_language._.technical_skills),
        #         'Soft_skills': list(self.resume_skills_language._.soft_skills),
        #     },
        #     "EDUCATION": self.resume_education._.education,
        #     "EXPERIENCE": self.resume_experience._.experiences,
        #     "LANGUAGES": list(self.resume_profile._.language),
        #     "PROJECTS": self.segmented_resume._.projects_segment,
        #     "REWARDS": self.segmented_resume._.rewards_segment,
        #     "REFERENCES": self.segmented_resume._.references_segment,
        # }
        json_data = {
            "PERSONAL_INFORMATION": personalInfo,
            "OBJECTIVE": self.segmented_resume._.objective_segment,
            "SKILLS":{
                'Skills': list(self.resume_skills_language._.technical_skills),
                'Soft_skills': list(self.resume_skills_language._.soft_skills),
            },
            "EDUCATION": self.resume_experience_academics._.experience_academics[1],
            "EXPERIENCE": self.resume_experience_academics._.experience_academics[0],
            "LANGUAGES": list(self.resume_profile._.language),
            "PROJECTS": self.segmented_resume._.projects_segment,
            "REWARDS": self.segmented_resume._.rewards_segment,
            "REFERENCES": self.segmented_resume._.references_segment,
        }
        return json_data

    def getStructuredData(self):
        '''
        This method will get all the required segmented part form a resume.
        Then the segmented part will be passed to their respective method and receive the required parsed information.

        :return: A JSON formatted data
        '''
        personal_information = self.profile_information_parser(self.segmented_resume._.profile_segment)
        # self.education_information_parser(self.segmented_resume._.academics_segment)
        # self.experience_information_parser(self.cleaned_resume)
        data_for_ner = "\n".join([self.segmented_resume._.objective_segment,self.segmented_resume._.skills_segment,self.segmented_resume._.links_segment,
                        self.segmented_resume._.experience_segment,self.segmented_resume._.language_segment,self.segmented_resume._.projects_segment,
                        self.segmented_resume._.rewards_segment,self.segmented_resume._.references_segment,self.segmented_resume._.academics_segment])
        self.experience_academics_parser(data_for_ner)
        self.skills_language_parser()

        # personal_information = self.personal_information_parser(self.segmented_resume._.profile_segment)        
        # objectives = self.segmented_resume._.objective_segment        
        # skills = self.skills_parser(self.segmented_resume._.skills_segment)        
        # academics = self.education_parser(self.segmented_resume._.academics_segment)        
        # experiences = self.experience_parser(self.segmented_resume._.experience_segment)        
        # language = self.language_parser(self.segmented_resume._.language_segment)        
        # projects = self.segmented_resume._.projects_segment        
        # rewards = self.segmented_resume._.rewards_segment        
        # references = self.segmented_resume._.references_segment
        # print (f"PERSONAL INFORMATION: {personal_information}\n")
        # print (f"OBJECTIVES : {objectives}\n")
        # print (f"SKILLS: {skills}\n")
        # print (f"ACADEMICS: {academics}\n")
        # print (f"EXPERIENCES: {experiences}\n")
        # print (f"LANGUAGES: {language}\n")
        # print (f"PROJECTS: {projects}\n")
        # print (f"REWARDS: {rewards}\n")
        # print (f"REFERENCES: {references}\n")
        formatted_data = self.returnjson(personal_information)
        return formatted_data


    def getScore(self,jd_path):
        '''
        This method will give us the similarity score between two documents i.e. resume and job description.
        Here, only "embedding_component" is enabled.

        :param jd_path: Path of the job description file
        :type jd_path: str
        :return: A similarity score which is between 0 and 1
        '''
        scorer = Word2VecScorer(cfg.word2vec_model)
        cleaned_jd = prepare_text(jd_path,dolower=False)
        # with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","academics_ner_parsing_component","experience_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component"):
        with self.spacy_pipeline.nlp.disable_pipes("category_component","segmentation_component","profile_ner_parsing_component","experience_academics_ner_parsing_component","profile_pattern_matching_component","skills_pattern_matching_component"):
            resume_embedding = self.spacy_pipeline.process_text(self.cleaned_resume)
            jd_embedding = self.spacy_pipeline.process_text(cleaned_jd)
        similarity_score = scorer.calculate_similarity(resume_embedding, jd_embedding)
        return similarity_score

    def rejectCV(self):
        '''
        This method will be executed if a given document is not a resume.
        '''
        return "This document is not a resume"


# test_doc = Parser()
# result = test_doc.identifyResume(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphin2\seven\dolphin\datasets\resumes\Ananya Jain BA Pharma2.docx")
# print (result)
