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
from domain_classification.domain_classification import DomainClassification


domain_classification_obj = DomainClassification()
score_generator_obj = Word2VecScorer(cfg.word2vec_model)
preprocessor_obj_for_score = PreprocessData()
NerObj = SpacyNer()
# helper_obj = NLTKHelper({"experience_type_a:{<VB>?<CD>?<N.*>?<IN>?<N.*|VBN|JJ>+<IN|VB.*>+<DT>?<JJ|VBG|N.*>+<CC>?<N.*>?}"})


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
    required_soft_skills = set(required_soft_skills)
    required_technical_skills = set(required_technical_skills)
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
        progress_score = slope * 10
        # print('Progress Score :', progress_score)
    else:
        progress_score = 0
        # print("Since your progress isn't promising your Progress Score is ", progress_score)

    return progress_score


def one_resume_multiple_jd_scorer(job, designations, user_exp, user_soft_skills, user_technical_skills, user_location, designation_dates):
    job_id = job.get('id')
    job_title = job.get('job_title')
    job_description = job.get('job_description')
    req_soft_skills, req_technical_skills, req_experience, all_designations, all_organizations, all_educations, all_locations = prepare_job_description(
        job_description)

    employer_city = job['location']['city']
    # employer_country = job['location']['country']
    # employer_state = job['location']['state']

    #Scoring on the basis of distance
    try:
        distance = calculate_distance(employer_city, user_location)
        # Normalizing to a range from 0 to 10
        distance_score = 5 - ((distance/20000)*5)
    except:
        distance_score = 5

    #Scoring on the basis of matching skills of user profile and jobs
    matched_soft_skills = user_soft_skills.intersection(req_soft_skills)
    matched_technical_skills = user_technical_skills.intersection(req_technical_skills)
 

    if matched_technical_skills != 0:
        try:
            technical_skill_score = len(matched_technical_skills) / len(req_technical_skills) * 35
        except:
            technical_skill_score = 35
    else:
        technical_skill_score = 0
    
        # skills score on basis of soft skills
    if matched_soft_skills != 0:
        try:
            soft_skills_score = len(matched_soft_skills) / len(req_soft_skills) * 5
        except:
            soft_skills_score = 5
    else:
        soft_skills_score = 0

    skill_score = technical_skill_score + soft_skills_score

    # designation score on the basis of matching and word2vec
    job_title = job_title.lower()
    designations = [desig.lower() for desig in designations]
    job_designations = [job_title] + all_designations
    user_designations = designations

    if len(job_designations) == 0 or len(user_designations) == 0:
        desig_score = 0
    else:
        if job_title in designations:
            desig_score = 40
        else:
            try:
                most_common_domain_user = domain_classification_obj.classify_domain_from_designation(user_designations)[0]
                most_common_domain_job = domain_classification_obj.classify_domain_from_designation(job_designations)[0]
                if most_common_domain_user == most_common_domain_job:
                    desig_score = 30
                else:
                    vector_score = []
                    for desig in designations:
                        desig_vec = score_generator_obj.get_word_embeddings(desig)
                        # print(str(user_id) + "---- User designation ---- {} \n".format(desig))
                        # print(str(user_id) + "---- job designation ---- {} \n".format(job_title))
                        job_title_vec = score_generator_obj.get_word_embeddings(job_title)
                        desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                            desig_vec, job_title_vec)
                        # print(str(user_id) + "---- Simialrity ---- {} \n".format(desig_job_title_similarity_desig))
                        vector_score.append(desig_job_title_similarity_desig)
                    try:
                        # Calculating average score for every designations
                        desig_job_title_similarity_designations = sum(
                            vector_score)/len(designations)
                    except:
                        desig_job_title_similarity_designations = 0
                    # Normalizing to range 0 to 40
                    desig_score = desig_job_title_similarity_designations * 40
            except:
                    vector_score = []
                    for desig in designations:
                        desig_vec = score_generator_obj.get_word_embeddings(desig)
                        job_title_vec = score_generator_obj.get_word_embeddings(job_title)
                        desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                            desig_vec, job_title_vec)
                        vector_score.append(desig_job_title_similarity_desig)
                    try:
                        # Calculating average score for every designations
                        desig_job_title_similarity_designations = sum(
                            vector_score)/len(designations)
                    except:
                        desig_job_title_similarity_designations = 0
                    # Normalizing to range 0 to 40
                    desig_score = desig_job_title_similarity_designations * 40


    #Calculating score on the basis of experience matching
    try:
        req_exp = " and ".join(req_experience)
        user_exp= " and ".join(user_exp) 
        # In case the chunking didn't extract any experience from job description
        if not req_exp or not user_exp:
            vec_sim = 0
        else:
            req_exp_vector = score_generator_obj.get_word_embeddings(req_exp)
            user_exp_vector = score_generator_obj.get_word_embeddings(user_exp)

            vec_sim = score_generator_obj.calculate_similarity(
                req_exp_vector, [user_exp_vector])

        # Normalizing to a range from 0 to 40
        experience_score = vec_sim * 5
    except:
        experience_score = 0

    # Scoring on the basis of progress of user
    try:
        if (not designation_dates):
            progress_score = 0
        else:
            progress_score = calculate_progress(designation_dates)
    except:
        progress_score = 10

    # If any nan values
    if np.isnan(experience_score):
        experience_score = 0
    if np.isnan(desig_score):
        desig_score = 0
    if np.isnan(skill_score):
        skill_score = 0
    if np.isnan(progress_score):
        progress_score = 0
    if np.isnan(distance_score):
        distance_score = 0

    total_score = experience_score + desig_score + skill_score + distance_score + progress_score
    return job_id, total_score


def one_JD_multiple_resume_scorer(profile, job_title,all_designations, req_exp, req_soft_skills, req_technical_skills, employer_city):
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
    

    #skill score on basis of technical skills matching
    if matched_technical_skills != 0:
        try:
            technical_skill_score = len(matched_technical_skills) / len(req_technical_skills) * 35
        except:
            technical_skill_score = 35
    else:
        technical_skill_score = 0

    # skills score on basis of soft skills
    if matched_soft_skills != 0:
        try:
            soft_skills_score = len(matched_soft_skills) / len(req_soft_skills) * 5
        except:
            soft_skills_score = 5
    else:
        soft_skills_score = 0

    skill_score = technical_skill_score + soft_skills_score

    # designation score on the basis of matching and word2vec
    job_title = job_title.lower()
    designations = [desig.lower() for desig in designations]
    job_designations = [job_title] + all_designations
    user_designations = designations

    if len(job_designations) == 0 or len(user_designations) == 0:
        desig_score = 0
    else:
        if job_title in designations:
            desig_score = 40
        else:
            try:
                most_common_domain_user = domain_classification_obj.classify_domain_from_designation(user_designations)[0]
                most_common_domain_job = domain_classification_obj.classify_domain_from_designation(job_designations)[0]
                if most_common_domain_user == most_common_domain_job:
                    desig_score = 30
                else:
                    vector_score = []
                    for desig in designations:
                        desig_vec = score_generator_obj.get_word_embeddings(desig)
                        # print(str(user_id) + "---- User designation ---- {} \n".format(desig))
                        # print(str(user_id) + "---- job designation ---- {} \n".format(job_title))
                        job_title_vec = score_generator_obj.get_word_embeddings(job_title)
                        desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                            desig_vec, job_title_vec)
                        # print(str(user_id) + "---- Simialrity ---- {} \n".format(desig_job_title_similarity_desig))
                        vector_score.append(desig_job_title_similarity_desig)
                    try:
                        # Calculating average score for every designations
                        desig_job_title_similarity_designations = sum(
                            vector_score)/len(designations)
                    except:
                        desig_job_title_similarity_designations = 0
                    # Normalizing to range 0 to 40
                    desig_score = desig_job_title_similarity_designations * 40
            except:
                    vector_score = []
                    for desig in designations:
                        desig_vec = score_generator_obj.get_word_embeddings(desig)
                        job_title_vec = score_generator_obj.get_word_embeddings(job_title)
                        desig_job_title_similarity_desig = score_generator_obj.calculate_similarity(
                            desig_vec, job_title_vec)
                        vector_score.append(desig_job_title_similarity_desig)
                    try:
                        # Calculating average score for every designations
                        desig_job_title_similarity_designations = sum(
                            vector_score)/len(designations)
                    except:
                        desig_job_title_similarity_designations = 0
                    # Normalizing to range 0 to 40
                    desig_score = desig_job_title_similarity_designations * 40

    #Calculating score on the basis of experience matching
    try:
        req_exp = " and ".join(req_exp)
        user_exp= " and ".join(user_exp) 
        # In case the chunking didn't extract any experience from job description
        if not req_exp or not user_exp:
            vec_sim = 0
        else:
            req_exp_vector = score_generator_obj.get_word_embeddings(req_exp)
            user_exp_vector = score_generator_obj.get_word_embeddings(user_exp)

            vec_sim = score_generator_obj.calculate_similarity(
                req_exp_vector, [user_exp_vector])

        # Normalizing to a range from 0 to 40
        experience_score = vec_sim * 5
    except:
        experience_score = 0

    # Calculate progress score of user profile acc to his experiences
    try:
        if (not designation_dates):
            progress_score = 0
        else:
            progress_score = calculate_progress(designation_dates)
    except:
        progress_score = 10

    # If any nan values convert to zero
    if np.isnan(experience_score):
        experience_score = 0
    if np.isnan(desig_score):
        desig_score = 0
    if np.isnan(skill_score):
        skill_score = 0
    if np.isnan(progress_score):
        progress_score = 0
    if np.isnan(distance_score):
        distance_score = 0

    total_score = experience_score + desig_score + skill_score + distance_score + progress_score
    print(str(user_id)+"--------------Designation score-----------------"+str(desig_score))
    print(str(user_id)+"--------------Progress-----------------"+str(progress_score))
    print(str(user_id)+"--------------Experience-----------------"+str(experience_score))
    print(str(user_id)+"-----------------Distance--------------"+str(distance_score))
    print(str(user_id)+"-----------------Designation--------------"+str(desig_score))
    print(str(user_id)+"-----------------Skills--------------"+str(skill_score))
    print(str(user_id)+"-----------------Total--------------"+str(total_score))
    return user_id, total_score
