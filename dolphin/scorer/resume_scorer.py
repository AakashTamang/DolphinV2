import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
# from pipeline import NlpPipeline
# from word2vec import Word2VecScorer
import settings as cfg
from datareader import prepare_text
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from sklearn.preprocessing import MinMaxScaler
from scipy import stats
# from settings import technical_skills_pool, soft_skills_pool
from scorer.helper import PreprocessData, NLTKHelper
from word2vec import Word2VecScorer
from job_parsing.jd_parsing import SpacyNer

score_generator_obj = Word2VecScorer(cfg.word2vec_model)

preprocessor_obj_for_score = PreprocessData()

# helper_obj = NLTKHelper({"experience_type_a:{<VB>?<CD>?<N.*>?<IN>?<N.*|VBN|JJ>+<IN|VB.*>+<DT>?<JJ|VBG|N.*>+<CC>?<N.*>?}"})
NerObj = SpacyNer()

# scorer = Word2VecScorer(cfg.word2vec_model)
java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

geolocator = Nominatim(user_agent="Dolphin")
# new_pipeline = NlpPipeline()
# adding embedding component
# new_pipeline.add_embedding_component()


def prepare_profile(profile):
    '''
    Takes user profile and filters
    only the necessary attributes
    for the score calculation
    :arg profile of user :type dict
    :returns technical skills,
    all_experiences :type set , list
    '''
    technical_skills = set(profile.get('technical_skills'))
    soft_skills = set(profile.get('soft_skills'))
    # skills = technical_skills.union(soft_skills)
    # technical_skills = set(profile.get('skills'))
    designations = []
    try:
        job_seeker_location = json.loads(profile['profile'])['address']['city']
    except:
        job_seeker_location = profile['profile']['address']['city']
    all_experiences = []
    designation_dates = []
    for xp in json.loads(profile.get('exps')):
        designation = xp.get('designation')
        entry_date = xp.get('entry_date')
        exit_date = xp.get('exit_date')
        if not entry_date:
            entry_date = datetime.today().strftime('%Y-%m-%d')
        if not exit_date:
            exit_date = datetime.today().strftime('%Y-%m-%d')
        entry_year = entry_date.split("-")[0]
        exit_year = exit_date.split("-")[0]
        years_of_exp = int(exit_year) - int(entry_year)
        designations.append(designation)
        all_experiences.append((str(years_of_exp) + ' years of' +
                                ' experience as '+designation))
        designation_dates.append((entry_date, designation))
        set(designations)
    return soft_skills, technical_skills, all_experiences, designations, job_seeker_location, designation_dates


def prepare_job_description(job_description):
    '''
    Takes the job description and
    extracts the skills and experience
    that falls under the job requirements
    :arg job_description
    :type str
    :returns required_skills,required_experiences
    :type set ,list
    '''

    required_technical_skills, required_soft_skills = NerObj.get_skills(
        job_description)
    all_designations, all_organizations, required_experience, all_educations, all_locations = NerObj.parse(
        job_description)

    return required_soft_skills, required_technical_skills, required_experience, all_designations, all_organizations, all_educations, all_locations


def calculate_distance(address1, address2):
    ''' 
    Gives distance between two locations
    params: address of first location
                adress of second location
    returns: distance between two address in kilometers
    '''
    location1, (latitude1, longitude1) = geolocator.geocode(address1)
    location2, (latitude2, longitude2) = geolocator.geocode(address2)
    distance = geodesic((latitude1, longitude1),
                        (latitude2, longitude2)).kilometers
    return distance


def calculate_progress(designation_dates):
    unique_data = list(set(designation_dates))
    uni_designations = []
    uni_dates = []
    for i in range(len(unique_data)):
        uni_dates.append(unique_data[i][0])
        uni_designations.append(unique_data[i][1])

    # add classifier here to normalize designation
    normailized_design = ['Junior Employee',
                          'Intermediate Employee', 'Employee', 'Senior Employee']

    corres_num = []
    for i in normailized_design:
        if(i == 'Intern'):
            corres_num.append(0)
        elif(i == 'Junior Employee'):
            corres_num.append(1)
        elif(i == 'Employee'):
            corres_num.append(2)
        elif(i == 'Senior Employee'):
            corres_num.append(3)

    list_data = []
    for i in range(len(uni_dates)):
        list_data.append((uni_dates[i], corres_num[i]))

    df = pd.DataFrame(list_data, columns=['Column1', 'Column2'])

    df['date_ordinal'] = pd.to_datetime(df['Column1']).map(datetime.toordinal)
    del df['Column1']

    together_conv = df.values.tolist()

    min_max_scaler = MinMaxScaler()

    norm_data = min_max_scaler.fit_transform(together_conv)
    final_norm = pd.DataFrame(norm_data, columns=['value', 'normalized_date'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        final_norm['normalized_date'], final_norm['value'])
    slope = slope - 0.0089661424386942
    # print(std_err)
    # slope ranges from (+1.0089661424386942 to -1.0089661424386942)

    if(slope > 0):
        progress_score = slope * 15
        print('Progress Score :', progress_score)
    else:
        progress_score = 0
        print("Since your progress isn't promising your Progress Score is ", progress_score)

    return progress_score


def one_resume_multiple_jd_scorer(job, designations, user_exp, user_soft_skills, user_technical_skills, user_location, designation_dates):
    job_id = job.get('id')
    job_title = job.get('job_title')
    job_description = job.get('job_description')
    req_soft_skills, req_technical_skills, req_experience, all_designations, all_organizations, all_educations, all_locations = prepare_job_description(
        job_description)

    #required_soft_skills, required_technical_skills, required_experience, all_designations, all_organizations, all_educations, all_locations
    employer_city = job['location']['city']
    # employer_country = job['location']['country']
    # employer_state = job['location']['state']
    try:
        distance = calculate_distance(employer_city, user_location)
        # Normalizing to a range from 0 to 10
        distance_score = 5 - ((distance/20000)*5)
    except:
        distance_score = 5

    matched_soft_skills = user_soft_skills.intersection(req_soft_skills)
    matched_technical_skills = user_technical_skills.intersection(req_technical_skills)
    try:
        skill_score = (len(matched_soft_skills)+(len(matched_technical_skills))
                       )/(len(req_technical_skills)+len(req_soft_skills)) * 25
    except:
        skill_score = 25

    if job_title in designations:
        desig_score = 40
    else:
        vector_score = []
        for desig in designations:
            desig_vec = score_generator_obj.get_word_embeddings(desig)
            job_title_vec = score_generator_obj.get_word_embeddings(job_title)
            desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                desig_vec, [job_title_vec])
            vector_score.append(desig_job_title_similarity_desig)

        # Calculating average score for every designations
        desig_job_title_similarity_designations = sum(
            vector_score)/len(designations)
        # Normalizing to range 0 to 40
        desig_score = desig_job_title_similarity_designations * 40

    # In case the chunking didn't extract any experience from job description
    if len(req_experience) == 0:
        req_experience = ['Minimum 1 years of experience as ' + job_title]
    
    # print('+++++++++++++++++++++++++++++++++++++++++++++')
    # print("req_exp :: ")
    # print(req_experience,type(req_experience))
    # print("user_exp :: ")
    # print(user_exp,type(user_exp))
    # print('+++++++++++++++++++++++++++++++++++++++++++++')

    req_exp_vector = score_generator_obj.get_word_embeddings(req_experience)
    user_exp_vector = score_generator_obj.get_word_embeddings(user_exp)

    # print('+++++++++++++++++++++++++++++++++++++++++++++')
    # print("req_exp_vec :: ")
    # print(req_exp_vector)
    # print("user_exp_vec :: ")
    # print(user_exp_vector)
    # print('+++++++++++++++++++++++++++++++++++++++++++++')

    vec_sim = score_generator_obj.calculate_similarity(
        req_exp_vector, [user_exp_vector])

    # Normalizing to a range from 0 to 40
    experience_score = vec_sim * 15

    if np.isnan(experience_score):
        experience_score = 0
    if np.isnan(desig_score):
        desig_score = 0
    if np.isnan(skill_score):
        skill_score = 0

    try:
        if (not designation_dates):
            progress_score = 0
        else:
            progress_score = calculate_progress(designation_dates)
    except:
        progress_score = 15

    total_score = experience_score + desig_score + skill_score + distance_score + progress_score
    # print("\n")
    # print("\n")
    # print("----------------------"+str(job_id)+"-------------------------")
    # print("exp"+str(experience_score))
    # print("desig"+str(desig_score))
    # print("skill"+str(skill_score))
    # print("distance"+str(distance_score))
    # print("progress"+str(progress_score))
    # print('--------------------------------------------------------------')
    # print("\n")
    # print("\n")
    return job_id, total_score


def one_JD_multiple_resume_scorer(profile, job_title, req_exp, req_soft_skills, req_technical_skills, employer_city):
    user_id = profile.get('user_id')
    user_soft_skills, user_technical_skills, user_exp, designations, user_location, designation_dates = prepare_profile(
        profile)
    user_soft_skills = [x.lower() for x in user_soft_skills]
    user_technical_skills = [x.lower() for x in user_technical_skills]
    req_soft_skills = [x.lower() for x in req_soft_skills]
    req_technical_skills = [x.lower() for x in req_technical_skills]
    matched_soft_skills = set(user_soft_skills).intersection(set(req_soft_skills))
    matched_technical_skills = set(
        user_technical_skills).intersection(set(req_technical_skills))

    ##For testing skills score relevance
    # print("\n\n")
    # print("Job Soft Skills --{} ---> {}".format(req_soft_skills, type(req_soft_skills)))
    # print("\n")
    # print("Job Technical Skills --{} ---> {}".format(req_technical_skills,
                                                     # type(req_technical_skills)))
    # skills_set = {user_id:{"user_soft_skills":user_soft_skills,"user_technical_skills":user_technical_skills,"matched_soft_skills":matched_soft_skills,"matched_technical_skills":matched_technical_skills}}
    # print("\n\n")
    # print(skills_set)

    # calculating score for distance
    try:
        distance = calculate_distance(employer_city, user_location)
        # Normalizing to a range from 0 to 10
        rounded_dist = round(distance)
        if(rounded_dist > 0):
            distance_score = 5 - (distance/20000*5)
        else:
            distance_score = 5
    except:
        distance_score = 5

    # calculating score for skills
    try:
        skill_score = (len(matched_soft_skills)+(len(matched_technical_skills))
                       )/(len(req_technical_skills)+len(req_soft_skills)) * 25
    except:
        skill_score = 25

    # calculating score for job designation
    if job_title in designations:
        desig_score = 40
    else:
        vector_score = []
        for desig in designations:
            desig_vec = score_generator_obj.get_word_embeddings(desig)
            job_title_vec = score_generator_obj.get_word_embeddings(job_title)
            desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                desig_vec, [job_title_vec])
            vector_score.append(desig_job_title_similarity_desig)
        try:
            # Calculating average score for every designations
            desig_job_title_similarity_designations = sum(
                vector_score)/len(designations)
        except:
            desig_job_title_similarity_designations = 0
        # Normalizing to range 0 to 40
        desig_score = desig_job_title_similarity_designations * 40

    # calculating scores for experience
    if len(req_exp) == 0 or len(user_exp) == 0:
        vec_sim = 0
    else:
        req_exp_vector = score_generator_obj.get_word_embeddings(req_exp)
        user_exp_vector = score_generator_obj.get_word_embeddings(user_exp)

        vec_sim = score_generator_obj.calculate_similarity(
            req_exp_vector, [user_exp_vector])

    # Normalizing to a range from 0 to 40
    experience_score = vec_sim * 15

    if np.isnan(experience_score):
        experience_score = 0
    if np.isnan(desig_score):
        desig_score = 0
    if np.isnan(skill_score):
        skill_score = 0

    try:
        if (not designation_dates):
            progress_score = 0
        else:
            progress_score = calculate_progress(designation_dates)
    except:
        progress_score = 15

    # print(str(user_id)+"-------------------------------"+str(progress_score))
    total_score = experience_score + desig_score + \
        skill_score + distance_score + progress_score

    # print("Required experiences :: {}".format(req_exp))
    # print("User experiences :: {}".format(user_exp))
    # print("Experience similarity : {}, Experience Score :: {}".format(
    #     vec_sim, experience_score))
    # print("Job Decription location :: {}  Job Seeker location :: {}  Distance score : {}".format(
    #     employer_city, user_location, distance_score))
    # print("Job titles {}".format(job_title))
    # print("Designations:  {}".format(designations))
    # print("Desig Score {}".format(desig_score))
    # print("Designation dates {}".format(designation_dates))
    # print("progress score {}".format(progress_score))
    return user_id, total_score
