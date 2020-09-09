import os
import json
import ast
import __init__
import concurrent.futures

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
from settings import word2vec_model
from mongoengine import connect
from mongo_orm.parsed_information import ParsedCollection
from mongo_orm.scored_information import ScoredDocuments
connect(db="resume_db", host='127.0.0.1', port=27017)

parser_save = ParsedCollection()
scorer_save = ScoredDocuments()

# java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
# os.environ['JAVAHOME'] = java_path

app = Flask(__name__)
CORS(app, headers="X-CSRFToken, Content-Type")

new_resume_parser_obj = newParser()
domain_classification_obj = DomainClassification()
parse_jd = SpacyNer()
word2vec_obj = Word2VecScorer(word2vec_model)


@app.route("/newparse", methods=["POST"])
def new_parse_cv():
    resume = request.files.get('resume')
    if resume:
        filename = resume.filename
        file = tempStorage + '/' + filename
        resume.save(file)
        parsed_user_data = new_resume_parser_obj.identifyResume(file)
        parser_save.education = parsed_user_data["EDUCATION"]
        parser_save.experience = parsed_user_data["EXPERIENCE"]
        parser_save.languages = parsed_user_data["LANGUAGES"]
        parser_save.objectives = parsed_user_data["OBJECTIVE"]
        parser_save.projects = parsed_user_data["PROJECTS"]
        parser_save.skills = parsed_user_data["SKILLS"]
        parser_save.rewards = parsed_user_data["REWARDS"]
        parser_save.references = parsed_user_data["REFERENCES"]
        parser_save.personal_information = parsed_user_data["PERSONAL_INFORMATION"]
        parser_save.save()
        parsed_user_data = json.dumps(parsed_user_data)
        return jsonify(parsed_user_data)


@app.route("/generatescoreprofile", methods=["POST", "GET"])
def oneResMultipleJD():
    form_data_ = request.get_json()
    user_profile = form_data_.get('user_profile')
    scorer_save.user_profile = user_profile
    user_skills, user_exp, designations, user_location, designation_dates = prepare_profile(
        user_profile)
    # user_id = user_profile.get('user_id')
    my_score = {}
    job_descriptions = list(json.loads(form_data_.get('jobs')))

    for jd in job_descriptions:
        scorer_save.job_description = jd
        scorer_save.save()
    # Multiprocessing because of heavy computational time
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = [executor.submit(one_resume_multiple_jd_scorer, job_description, designations, user_exp,
                                  user_skills, user_location, designation_dates) for job_description in job_descriptions]
    my_score = {}
    imp_words = {}
    final_result = {}

    for f in concurrent.futures.as_completed(result):
        id, total_score,job_title,req_soft_skills,req_technical_skills,req_experience,employer_city,employer_state,employer_country = f.result()
        my_score[id] = total_score
        words = [job_title,req_soft_skills,req_technical_skills,req_experience,employer_city,employer_state,employer_country]
        imp_words[id] = words
    final_result["scores"] = my_score
    final_result["imp_words"] = imp_words 
    return final_result


@app.route("/generatescorejobdescription", methods=["POST", "GET"])
def oneJDMultipleRes():
    form_data_ = request.get_json()
    job = ast.literal_eval(form_data_.get('job'))
    job_id = job.get('id')
    scorer_save.job_description = job
    job_title = job.get('job_title')
    job_description = job.get('job_description')
    employer_city = job['location']['city']
    employer_country = job['location']['country']
    employer_state = job['location']['state']
    # print(job_description)
    req_soft_skills, req_technical_skills, req_experience = prepare_job_description(
        job_description)
    user_profiles = form_data_.get('user_profiles')
    for up in user_profiles:
        scorer_save.user_profile = up
        scorer_save.save()
    # In case the job_parsing module didn't extract any experience from job description
    if len(req_experience) == 0:
        req_experience = 'Experience in ' + job_title

    # Multiprocessing because of heavy computational time
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(one_JD_multiple_resume_scorer, profile, job_title, req_experience,
                                   req_soft_skills, req_technical_skills, employer_city) for profile in user_profiles]
    my_score = {}
    final_result = {}
    imp_words = {}

    for f in concurrent.futures.as_completed(results):
        id, total_score = f.result()
        my_score[id] = total_score
    imp_words[job_id] = [job_title,req_soft_skills,req_technical_skills,req_experience,employer_city,employer_state,employer_country]
    final_result["scores"] = my_score
    final_result["imp_words"] = imp_words
    
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
        most_common_domain = json.dumps(most_common_domain)
        return jsonify(most_common_domain)


@app.route('/parsejd', methods=['POST'])
def parsing_jd():
    document = request.files.get('job_description')
    if document:
        filename = document.filename
        file = tempStorage + '/' + filename
        document.save(file)
        jd_parsed_result = parse_jd.clean_parse_jd(file)
        jd_parsed_result = json.dumps(jd_parsed_result)
        return jsonify(jd_parsed_result)


@app.route("/generatescore", methods=["POST", "GET"])
def get_score_for_resume_and_jd():
    """
    Function for generating score of job descriptions from file content
    """
    resume = request.files.get('resume')
    if resume:
        filename = resume.filename
        file = tempStorage + '/' + filename
        resume.save(file)
        # job_description = request.form.get('jobs')#from django
        job_descriptions = (request.form.get('jobs'))
        if type(job_descriptions) == str:
            job_descriptions = ast.literal_eval(job_descriptions)
        else:
            pass
        response = word2vec_obj.calculate_score(file, job_descriptions)
        return jsonify(response)

@app.route("/matcher",methods = ["POST","GET"])
def galeShapelyAlgo():
    form_data_ = request.get_json()
    oneJD_MultipleRes_Score = form_data_.get('oneJD_MultipleRes_Score')
    oneRes_MultipleJD_Score = form_data_.get('oneRes_MultipleJD_Score')

    hiredobj = matcher(oneJD_MultipleRes_Score, oneRes_MultipleJD_Score)
    hired = hiredobj.matchmaker()
    result = {"results":['  ' + ',\n  '.join('%s is hired by %s' % match for match in sorted(hired.items()))]}
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002, debug=True)
