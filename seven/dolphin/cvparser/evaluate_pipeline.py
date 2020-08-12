import time
import glob
import cProfile, pstats, io
import os
import json

from datareader import prepare_text,clean_text

from pipeline import NlpPipeline
from word2vec import Word2VecScorer
import settings as cfg

scorer = Word2VecScorer(cfg.word2vec_model)

java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

# resume_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphinlab\aakash_resume_data\Ananya Jain BA Pharma.docx", dolower=False)
# doc = nlp(resume_content)
pr = cProfile.Profile()
pr.enable()
resume_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphin2\seven\dolphin\datasets\resumes\Ananya Jain BA Pharma2.docx", dolower=False)

# jd_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphin2\seven\dolphin\datasets\jobs\Cyber Security.docx", dolower=False)

# other_content = prepare_text(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphin2\seven\dolphin\datasets\other\news.docx", dolower=False)

new_pipeline = NlpPipeline()

# adding segmentation to pipeline
new_pipeline.add_segmentation_component()

# adding standford ner tagging to pipeline
new_pipeline.add_ner_parsing()

# adding document categorization to pipeline
# new_pipeline.add_category_component()

# adding embedding component
new_pipeline.add_embedding_component()

# adding pattern matching to pipeline
# new_pipeline.add_pattern_matching()

'''
Here we will pass names of the pipeline components that we want to disable. Afterh the completion of the taks,
all the pipeline components will be resotred back
'''
# print("1. NLP Pipelines available {}".format(new_pipeline.nlp.pipe_names))
# with new_pipeline.nlp.disable_pipes("ner_parsing_component","segmentation_component","embedding_component","pattern_matching_component"):
#     print("2. NLP Pipelines available {}".format(new_pipeline.nlp.pipe_names))
#     result = new_pipeline.process_text(resume_content)

# print("3. NLP Pipelines available {}".format(new_pipeline.nlp.pipe_names))

result = new_pipeline.process_text(resume_content)


# result2 = new_pipeline.process_text(jd_content)
# result3 = new_pipeline.process_text(other_content)

# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# with open(r'cprofile reports\halka_ramialo.txt','w') as f:
#     f.write(s.getvalue())


# for testing multiple resumes
# new_pipeline = nlp_pipeline()
# new_pipeline.add_segmentation_component()
# new_pipeline.add_ner_parsing()
# new_pipeline.add_pattern_matching()
# new_pipeline.add_category_component()
# files = glob.glob(r'datasets\resumes\test\*')
# pr = cProfile.Profile()
# pr.enable()
# for filename in files:
#     print (filename)
#     # line of code
#     resume_content = prepare_text(filename, dolower=False)
#     new_pipeline.process_text(resume_content)
# # doc = nlp(resume_content)
# # result = new_pipeline.process_text(resume_content)
# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# # print (s.getvalue())
# with open(r'cprofile reports\class_multiple_2.txt','w') as f2:
#     f2.write(s.getvalue())

# print("NLP Pipelines available {}".format(new_pipeline.nlp.pipe_names))
# print("Category of Resume document -----> {}".format(result._.category))
# print("Category of Job Description document -----> {}".format(result2._.category))
# print("Category of Other document -----> {}".format(result3._.category))
# print("Personal Profile ----> Name--> {} Address---> {}".format(result._.name,result._.address))
# print("Github ----> {}".format(result._.github))
# print("Linkedin ----> {}".format(result._.linkedin))
# print("Zipcode ----> {}".format(result._.zipcode))
# print("Technical Skills extracted ------> {}".format(result._.technical_skills))
# print("Soft Skills extracted ---------> {}".format(result._.soft_skills))
# print("Education -----> {}".format(result._.education))
# print("Experiences --------> {}".format(result._.experiences))
# print("Language extracted --------> {}".format(result._.language))
# print("Nationality Extracted -----> {}".format(result._.nationality))
# print("Emails Extracted -----> {}".format(result._.emails))
# print("Gender Extracted {}".format(result._.gender))
# print("Dates Extracted {}".format(result._.date))
# print("Phone Extracted {}".format(result._.phone))
# print()
# print ("---------------------------")
# print()
# print ("Profile: ", result._.profile_segment)
# print ("Objective: ", result._.objective_segment)
# print ("Skills: ", result._.skills_segment)
# print ("Academics: ", result._.academics_segment)
# print ("Experience: ", result._.experience_segment)
# print ("Language: ", result._.language_segment)
# print ("Projects: ", result._.projects_segment)
# print ("Rewards: ", result._.rewards_segment)
# print ("References: ", result._.references_segment)
# print ("Links: ", result._.links_segment)
# print()
# print ("---------------------------")
# print()
<<<<<<< HEAD:seven/dolphin/cvparser/evaluate_pipeline.py
# print("Embedding ------> ")
# embedding_from_resume = result._.embedding
# embedding_from_jd = result2._.embedding
# embedding_from_other = result3._.embedding
# resume_jd_match_score = scorer.calculate_similarity(embedding_from_resume, embedding_from_jd)
# resume_other_match_score = scorer.calculate_similarity(embedding_from_resume, embedding_from_other)
# jd_other_match_score = scorer.calculate_similarity(embedding_from_jd, embedding_from_other)
# print("Matching score Resume and JD: ", resume_jd_match_score)
# print("Matching score Resume and Other: ", resume_other_match_score)
# print("Matching score JD and Other: ", jd_other_match_score)

print("Embedding ------> ")
embedding_from_resume = result._.embedding
embedding_from_jd = result2._.embedding
embedding_from_other = result3._.embedding
resume_jd_match_score = scorer.calculate_similarity(embedding_from_resume, embedding_from_jd)
resume_other_match_score = scorer.calculate_similarity(embedding_from_resume, embedding_from_other)
jd_other_match_score = scorer.calculate_similarity(embedding_from_jd, embedding_from_other)
print("Matching score Resume and JD: ", resume_jd_match_score)
print("Matching score Resume and Other: ", resume_other_match_score)
print("Matching score JD and Other: ", jd_other_match_score)
# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# with open(r'cprofile reports\halka_ramialo.txt','w') as f:
#     f.write(s.getvalue())

