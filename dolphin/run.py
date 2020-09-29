import os
import json
import ast
import __init__
import concurrent.futures
from werkzeug.datastructures import ImmutableMultiDict
from flask import Flask, request, jsonify
from flask_cors import CORS
from datareader import prepare_text, prepare_text_from_string
from cvparser.newParse import Parser as newParser
from settings import tempStorage
from scorer.resume_scorer import prepare_profile, one_resume_multiple_jd_scorer, prepare_job_description, one_JD_multiple_resume_scorer
from domain_classification.domain_classification import DomainClassification
from job_parsing.jd_parsing import SpacyNer
from word2vec import Word2VecScorer
from matcher.match import matcher
import settings as cfg
from data_preprocessing import PreprocessData
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
# from mongoengine import connect
# from mongo_orm.parsed_information import ParsedCollection
# from mongo_orm.scored_information import ScoredDocuments
# connect(db="resume_db", host='127.0.0.1', port=27017)

# parser_save = ParsedCollection()
# scorer_save = ScoredDocuments()

# java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
# os.environ['JAVAHOME'] = java_path

app = Flask(__name__)
CORS(app, headers="X-CSRFToken, Content-Type")

new_resume_parser_obj = newParser()
domain_classification_obj = DomainClassification()
parse_jd = SpacyNer()
word2vec_obj = Word2VecScorer(cfg.word2vec_model)
preprocessor_obj = PreprocessData()

@app.route("/parse", methods=["POST"])
def new_parse_cv():
    resume = request.files.get('resume')
    if resume:
        filename = resume.filename
        file = tempStorage + '/' + filename
        resume.save(file)
        parsed_user_data = new_resume_parser_obj.identifyResume(file)
        # parser_save.education = parsed_user_data["EDUCATION"]
        # parser_save.experience = parsed_user_data["EXPERIENCE"]
        # parser_save.languages = parsed_user_data["LANGUAGES"]
        # parser_save.objectives = parsed_user_data["OBJECTIVE"]
        # parser_save.projects = parsed_user_data["PROJECTS"]
        # parser_save.skills = parsed_user_data["SKILLS"]
        # parser_save.rewards = parsed_user_data["REWARDS"]
        # parser_save.references = parsed_user_data["REFERENCES"]
        # parser_save.personal_information = parsed_user_data["PERSONAL_INFORMATION"]
        # parser_save.save()
        return jsonify(parsed_user_data)


@app.route("/generatescoreprofile", methods=["POST", "GET"])
def oneResMultipleJD():
    form_data_ = request.get_json()
    user_profile = form_data_.get('user_profile')
    # scorer_save.user_profile = user_profile
    user_soft_skills, user_technical_skills, user_exp, designations, user_location, designation_dates = prepare_profile(
        user_profile)
    job_descriptions = list(json.loads(form_data_.get('jobs')))

    # for jd in job_descriptions:
    #     scorer_save.job_description = jd
    #     scorer_save.save()
    # Multiprocessing because of heavy computational time

    progress_pool = pd.read_csv(cfg.progress_pool, sep=",")
            
    senior_pool_list = []
    junior_pool_list = []
    intermediate_pool_list = []
    manager_pool_list = []

    for i in range(len(progress_pool["Designations"])):
        val = progress_pool["Label"][i]
        desig = progress_pool["Designations"][i].lower().strip()
        if(val=="Junior"):
            junior_pool_list.append(desig)
        elif(val=="Senior"):
            senior_pool_list.append(desig)
        elif(val=="Intermediate"):
            intermediate_pool_list.append(desig) 
        elif(val=="Manager"):
            manager_pool_list.append(desig)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = [executor.submit(one_resume_multiple_jd_scorer, job_description, designations, user_exp,
                                  user_soft_skills, user_technical_skills, user_location, designation_dates, junior_pool_list, 
                                  intermediate_pool_list, senior_pool_list, manager_pool_list) for job_description in job_descriptions]
    my_score = {}
    missing_words_dict = {}
    final_result = {}

    for f in concurrent.futures.as_completed(result):
        id, total_score, missing_words = f.result()
        my_score[id] = total_score
        missing_words_dict[id] = missing_words

    final_result["scores"] = my_score
    final_result["missing_words"] = missing_words_dict

    return final_result


@app.route("/generatescorejobdescription", methods=["POST", "GET"])
def oneJDMultipleRes():
    form_data_ = request.get_json()
    job = ast.literal_eval(form_data_.get('job'))
    # job_id = job.get('id')
    # scorer_save.job_description = job

    job_title = job.get('job_title')
    job_description = job.get('job_description')
    employer_city = job['location']['city']
    # employer_country = job['location']['country']
    # employer_state = job['location']['state']

    req_soft_skills, req_technical_skills, required_experience, all_designations, all_organizations, all_educations, all_locations = prepare_job_description(
        job_description)


    user_profiles = form_data_.get('user_profiles')
    # for up in user_profiles:
    #     scorer_save.user_profile = up
    #     scorer_save.save()
    # In case the job_parsing module didn't extract any experience from job description
    if len(required_experience) == 0:
        required_experience = ['Experience in ' + job_title]

    progress_pool = pd.read_csv(cfg.progress_pool, sep=",")
            
    senior_pool_list = []
    junior_pool_list = []
    intermediate_pool_list = []
    manager_pool_list = []

    for i in range(len(progress_pool["Designations"])):
        val = progress_pool["Label"][i]
        desig = progress_pool["Designations"][i].lower().strip()
        if(val=="Junior"):
            junior_pool_list.append(desig)
        elif(val=="Senior"):
            senior_pool_list.append(desig)
        elif(val=="Intermediate"):
            intermediate_pool_list.append(desig) 
        elif(val=="Manager"):
            manager_pool_list.append(desig)

    # Multiprocessing because of heavy computational time
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(one_JD_multiple_resume_scorer, profile, job_title,all_designations, required_experience,
                                   req_soft_skills, req_technical_skills, employer_city, junior_pool_list, 
                                  intermediate_pool_list, senior_pool_list, manager_pool_list) for profile in user_profiles]
    my_score = {}
    missing_words_dict = {}
    final_result = {}

    for f in concurrent.futures.as_completed(results):
        id, total_score, missing_words = f.result()
        my_score[id] = total_score
        missing_words_dict[id] = missing_words

    soft_monograms = []
    soft_ngrams = []
    tech_monograms = []
    tech_ngrams = []

    for i in req_soft_skills:
        if(len(word_tokenize(i))>1):
            soft_ngrams.append(i)
        else:
            soft_monograms.append(i)

    for j in soft_ngrams:
        words = word_tokenize(j)
        for k in words:
            if k in soft_monograms:
                soft_monograms.remove(k)

    for i in req_technical_skills:
        if(len(word_tokenize(i))>1):
            tech_ngrams.append(i)
        else:
            tech_monograms.append(i)

    for j in tech_ngrams:
        words = word_tokenize(j)
        for k in words:
            if k in tech_monograms:
                tech_monograms.remove(k)

    imp_words = []
    imp_words = soft_monograms+soft_ngrams+tech_monograms+tech_ngrams
    
    if(all_educations):
        imp_words = imp_words+all_educations
    if(all_locations):
        imp_words = imp_words+all_locations
    if(all_designations):
        imp_words = imp_words+ all_designations
    if(all_organizations):
        imp_words = imp_words+all_organizations
    if(required_experience):
        imp_words = imp_words+required_experience
    # print("Job Title --{} ---> {}".format(job_title, type(job_title)))
    # print("Job Soft Skills --{} ---> {}".format(req_soft_skills, type(req_soft_skills)))
    # print("Job Technical Skills --{} ---> {}".format(req_technical_skills, type(req_technical_skills)))
    # print("Job Experience --{} ---> {}".format(required_experience, type(required_experience)))
    # print("Job Education --{} ---> {}".format(all_educations, type(all_educations)))
    # print("Job location --{} ---> {}".format(all_locations, type(all_locations)))
    # print("Job designation --{} ---> {}".format(all_designations, type(all_designations)))
    # print("Job organization --{} ---> {}".format(all_organizations, type(all_organizations)))
    final_result["scores"] = my_score
    final_result["imp_words"] = imp_words
    final_result["missing_words"] = missing_words_dict
    return final_result


@app.route('/domainclassification', methods=['POST'])
def classify_domain():
    document = request.files.get('job_description')
    if document:
        filename = document.filename
        file = tempStorage + '/' + filename
        document.save(file)
        most_common_domain = domain_classification_obj.clean_classify_document(
            file)
        return jsonify(most_common_domain)


@app.route('/parsejd', methods=['POST'])
def parsing_jd():
    document = request.files.get('job_description')
    if document:
        filename = document.filename
        file = tempStorage + '/' + filename
        document.save(file)
        jd_parsed_result = parse_jd.clean_parse_jd(file)
        return jsonify(jd_parsed_result)


@app.route("/generatescore", methods=["POST", "GET"])
def get_score_for_resume_and_jd():
    """
    Function for generating score of job descriptions from file content
    """
    resume = request.files.get('resume')
    jobs = ImmutableMultiDict(request.form)
    jobs = jobs.to_dict(flat=False)
    job_descriptions = jobs.get('jobs')
    # job_descriptions = request.form.get('jobs')
    if resume:
        filename = resume.filename
        file = tempStorage + '/' + filename
        resume.save(file)
        if type(job_descriptions) == str:
            job_descriptions = ast.literal_eval(job_descriptions)
        else:
            pass
        # sim_score = word2vec_obj.calculate_score(file,job_descriptions)
        # response = sim_score
        resume_content = prepare_text(file, dolower=False)
        preprocessed_resume_content = preprocessor_obj.preprocess_text(
            resume_content)
        preprocessed_resume_content = " ".join(preprocessed_resume_content)
        res_technical_skills, res_soft_skills = parse_jd.get_skills_from_pool(preprocessed_resume_content)
        res_technical_skills = set(res_technical_skills)
        res_soft_skills = set(res_soft_skills)
        resume_vector = word2vec_obj.get_word_embeddings(preprocessed_resume_content)
        score = {}
        for jd in job_descriptions:
            if type(jd) == str:
                jd = ast.literal_eval(jd)
            else:
                pass
            job_description = jd['job_description']
            job_text = preprocessor_obj.preprocess_text(job_description)
            job_text = " ".join(job_text)
            jd_technical_skills, jd_soft_skills = parse_jd.get_skills_from_pool(job_text)
            jd_technical_skills = set(jd_technical_skills)
            jd_soft_skills = set(jd_soft_skills)

            matched_soft_skills = res_soft_skills.intersection(jd_soft_skills)
            matched_technical_skills = res_technical_skills.intersection(jd_technical_skills)

            if matched_technical_skills != 0:
                try:
                    technical_skill_score = len(matched_technical_skills) / len(jd_technical_skills) * 35
                except:
                    technical_skill_score = 35
            else:
                technical_skill_score = 0
            
            if matched_soft_skills != 0:
                try:
                    soft_skills_score = len(matched_soft_skills) / len(jd_soft_skills) * 5
                except:
                    soft_skills_score = 5
            else:
                soft_skills_score = 0
            
            skill_score = technical_skill_score + soft_skills_score
            
            job_vector = word2vec_obj.get_word_embeddings(job_text)
            similarity = word2vec_obj.calculate_similarity(job_vector, resume_vector)
            if np.isnan(similarity):
                similarity = 0
            word2vecscore = int(similarity*60)
            score[jd['pk']] = word2vecscore + skill_score
        return jsonify(score)


@app.route("/getjobscore", methods=["POST", "GET"])
def get_score_for_jobs():
    """
    Function for generating score of job descriptions from file content
    """
    # import pdb;pdb.set_trace()
    # data = ImmutableMultiDict(request.form)
    # data = data.to_dict(flat=False)
    # primary_job = data.get('primary_job')[0]
    primary_job = request.json.get('primary_job')
    if type(primary_job) == str:
        primary_job = ast.literal_eval(primary_job)
    else:
        pass
    primary_job_title = primary_job['job_title']
    primary_job_description = primary_job['job_description']
    if primary_job:
        # other_jobs = data.get('other_jobs')[0]
        other_jobs = request.json.get('other_jobs')
        if type(other_jobs) == str:
            other_jobs = ast.literal_eval(other_jobs)
        else:
            pass
        # response = word2vec_obj.calculate_score(file, job_descriptions)
        response = word2vec_obj.score_jobs(primary_job_description,primary_job_title,other_jobs)
        return jsonify(response)


@app.route("/matcher", methods=["POST", "GET"])
def galeShapelyAlgo():
    form_data_ = request.get_json()
    oneJD_MultipleRes_Score = form_data_.get('oneJD_MultipleRes_Score')
    oneRes_MultipleJD_Score = form_data_.get('oneRes_MultipleJD_Score')

    hiredobj = matcher(oneJD_MultipleRes_Score, oneRes_MultipleJD_Score)
    hired = hiredobj.matchmaker()
    result = {"matches":[[j,i] for i,j in sorted(hired.items())]}
    return result


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)
