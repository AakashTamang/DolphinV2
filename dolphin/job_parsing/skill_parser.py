import pandas as pd
from job_parsing.createngrams import get_ngrams
from settings import technical_skills_pool, soft_skills_pool

def capitalizeinput(inputparameter):
    '''
    This will take the raw input text and
    tokenize the string and capitalize all
    the token and returns the formatted
    capitalized text.
    :param inputparameter :type str
    :return: string(text will all the tokens capitalized)
    '''
    formatted_output = inputparameter.title()
    return formatted_output

def technical_skills_parser(jd_doc):
    '''
    This function here extracts all the possible
    skill present in the resume. It does so by
    comparing the predefined skills tokens and
    bigrams with the tokens and bigrams of the resume.
    :param jd_doc: spaCy doc
    :return: This returns the capitalized skills in
            the form of list of str.
    '''
    skillbigrams = get_ngrams(jd_doc,2)
    skill_tokens = [token.text for token in jd_doc]
    skills = pd.read_csv(technical_skills_pool)
    skillbigrams.extend(skill_tokens)
    total_skills = [skill.lower() for skill in skillbigrams]
    skills['matched'] = skills['Predefined_skills'].apply(lambda x: 1 if x.lower() in total_skills else 0)
    matched_skills = skills.Predefined_skills.loc[skills['matched'] == 1].values
    matched_skills = matched_skills.tolist()
    formatted_skills = map(capitalizeinput, matched_skills)
    return [skill for skill in formatted_skills]

def soft_skills_parser(jd_doc):
    '''
    This function here extracts all the possible
    soft skills present in the resume. It does so by
    comparing the predefined soft skills tokens and
    bigrams with the tokens and bigrams of the resume.
    :param jd_doc: spaCy doc
    :return: This returns the capitalized soft skills in
            the form of list of str.
    '''
    soft_skill_bigrams = get_ngrams(jd_doc,2)
    soft_skill_trigrams = get_ngrams(jd_doc,3)
    soft_skill_tokens = [token.text for token in jd_doc]
    soft_skill_bigrams.extend(soft_skill_trigrams)
    soft_skill_tokens.extend(soft_skill_bigrams)
    total_skills = [skill.lower() for skill in soft_skill_tokens]
    predefined_skills_df = pd.read_csv(soft_skills_pool)
    predefined_skills_df['matched'] = predefined_skills_df['Predefined_skills'].apply(lambda x: 1 if x.lower() in total_skills else 0)
    matched_soft_skills = predefined_skills_df.Predefined_skills.loc[predefined_skills_df['matched']==1].values
    matched_soft_skills = matched_soft_skills.tolist()
    formatted_soft_skills = map(capitalizeinput, matched_soft_skills)
    return [skill for skill in formatted_soft_skills]
