import re
import string
import datetime

import datefinder
from cvparser.formatter.standarizedata import comparedates
# from formatter.standarizedata import comparedates

def key_value_formatter(list_kv):
    syn_name = ['Name', 'name']
    syn_birthdate = ['D.O.B', "Date of Birth", "Birthdate", "Birth date", "D-O-B"]
    syn_address = ['Address', 'Location', 'address']
    rule = r'[^:|\s|\n|-]+[A-Za-z0-9\s/.,@-]+'
    key_value_pair = {}
    name_value = []
    date_value = []
    location_value = []
    for token in list_kv:
        result = re.findall(rule, token)
        if len(result) == 2:
            key = result[0]
            if key in syn_name:
                name_value.append(result[1])
                key_value_pair.update({key: name_value})
            elif key in syn_birthdate:
                key = "D.O.B"
                date_value.append(result[1])
                key_value_pair.update({key: date_value})
            elif key in syn_address:
                key = "Address"
                location_value.append(result[1])
                key_value_pair.update({key: location_value})
    return key_value_pair


def key_value_identifier(text):
    rule = r'[A-Za-z\.][:|-|:-][^\n]+'
    result = re.findall(rule, text)
    result = key_value_formatter(result)
    return result

def cleandata(sentence):
    cleanedsent = sentence.translate(str.maketrans('', '', string.punctuation))
    cleanedsent =cleanedsent.strip()
    cleanedsent = cleanedsent.lower()
    cleanedsent = (cleanedsent.split())
    cleanedsent =  ' '.join(cleanedsent)
    return (re.sub(r' +',' ',cleanedsent))


def formatPersonalinfo(personal_info):
    '''
    This functions takes all the unstructured personal information and returns the formatted and structured
    personal information.
    :param personal_info: (List) of all the fields required as personal info.
    :return: List(Returns the formatted personal info will all the required fields.)
    '''
    personalInfo = {}
    personal_title = [
                     'name',
                     'Address',
                     'Email',
                     'Phone_Number',
                     'Zip_Code',
                     'Nationality',
                     'github',
                     'linkedin',
                     'birthdate',
                     'Gender'
                      ]
    for arg,title in zip(personal_info,personal_title):
        if title == 'name':
            name_tokens = arg.split(' ')
            if len(name_tokens)>=3:
                personalInfo.update({'First_Name':name_tokens[0]})
                personalInfo.update({'Last_Name':name_tokens[-1]})
                personalInfo.update({'Middle_Name':name_tokens[1]})
            else:
                personalInfo.update({'First_Name': name_tokens[0]})
                personalInfo.update({'Last_Name': name_tokens[-1]})
        else:
            personalInfo.update({title:arg})
    return personalInfo


def formatEducationalinfo(sent_tokens, sent2idx, alldegree,
                        alluniversity, alldate, alllocations):
    unique_identifier = 0
    degree_index = []
    university_index = []
    date_index = []
    location_index = []
    formatted_academics = {}
    item_tracker = {}
    for sentence in sent_tokens:
        cleaned_sentence = cleandata(sentence)
        for degree in alldegree:
            cleaned_degree = cleandata(degree)
            if cleaned_degree in cleaned_sentence:
                if cleaned_degree not in item_tracker:
                    item_tracker.update({cleaned_degree:1})
                    degree_index.append((degree,sent2idx[cleaned_sentence]))


                elif cleaned_degree in item_tracker:
                    if cleaned_degree == cleaned_sentence:
                        key = cleaned_sentence+'{}'.format(item_tracker[cleaned_degree])

                        degree_index.append((degree,sent2idx[key]))
                    else:
                        degree_index.append((degree,sent2idx[cleaned_sentence]))
                alldegree.remove(degree)
                break



        for university in alluniversity:
            cleaned_university = cleandata(university)
            if cleaned_university in cleaned_sentence:
                if cleaned_university not in item_tracker:
                    university_index.append((university,sent2idx[cleaned_sentence]))
                    item_tracker.update({cleaned_university:1})

                elif cleaned_university in item_tracker:

                    key = cleaned_sentence+'{}'.format(item_tracker[cleaned_university])
                    university_index.append((university,sent2idx[key]))
                alluniversity.remove(university)
                break

        for date in alldate:
            if date in sentence:
                found_date = []
                try:
                    found_date = [d for d in datefinder.find_dates(date)]
                except:
                    pass

                if found_date:
                    formatted_date = found_date[0].strftime("%d-%m-%Y")
                    date_index.append((formatted_date, sent2idx[cleaned_sentence]))
                alldate.remove(date)

        for location in alllocations:
            cleaned_location = cleandata(location)
            if cleaned_location in cleaned_sentence:
                if cleaned_location not in item_tracker:
                    location_index.append((location, sent2idx[cleaned_sentence]))
                    item_tracker.update({cleaned_location:1})

                elif cleaned_location in item_tracker:
                    if cleaned_location == cleaned_sentence:
                        key = cleaned_sentence +'{}'.format(item_tracker[cleaned_location])
                        location_index.append((location,sent2idx[key]))
                    else:
                        location_index.append((location,sent2idx[cleaned_sentence]))
                    alllocations.remove(location)

                break




    for i in range(len(degree_index)-1):
        j = i+1
        if degree_index[i][1] == degree_index[j][1]:

            new_degree = ((degree_index[i][0]+' '+ degree_index[j][0]))
            new_index = degree_index[i][1]
            degree_index.remove((degree_index[i][0],degree_index[i][1]))
            degree_index.remove((degree_index[i][0],degree_index[i][1]))
            degree_index.append((new_degree,new_index))
            degree_index.append(('dummy',1000))

    for i in range(len(university_index)-1):
        j = i+1
        if university_index[i][1] == university_index[j][1]:
            new_university = ((university_index[i][0]+' ' +university_index[j][0]))
            new_index = university_index[i][1]
            university_index.remove((university_index[i][0],university_index[i][1]))
            university_index.remove((university_index[i][0],university_index[i][1]))
            university_index.append((new_university,new_index))
            university_index.append(('dummy',100))

    bachelor_degree = ["Bachelors", "Bachelor","Bachelor's"]
    master_degree = ["Masters","Master's","Master"]
    phd_degree = ["PHD", "PhD"]
    words = ["Bachelors","Bachelor","Bachelor's","Masters","Master","Master's","PHD","PhD","Degree","degree","in","of"]

    for degree,degindex in degree_index:

        academic_cluster = {}
        if degree != 'dummy':
            if degree.split(" ")[0] in bachelor_degree:
                academic_cluster.update({"degree":"B"})
            elif degree.split(" ")[0] in master_degree:
                academic_cluster.update({"degree":"M"})
            elif degree.split(" ")[0] in phd_degree:
                academic_cluster.update({"degree":"P"})
            for i in words:
                if i in degree:
                    degree = degree.replace(i,"").strip()
            academic_cluster.update({"program":degree})
        for university,unindex in university_index:
            if abs(degindex - unindex) <= 2:
                academic_cluster.update({'institution':university})
        # for location,locindex  in location_index:
        #     if abs(degindex - locindex) <= 2:
        #         academic_cluster.update({'location':location})
        possible_dates = []
        new_date_index = 0
        for date,dateindex in date_index:
            if abs(degindex - dateindex ) <=3:
                new_date_index = dateindex
                possible_dates.append(date)

            elif abs(new_date_index - dateindex) < 2:
                possible_dates.append(date)
        if len(possible_dates)>=2:
            exit_date,entry_date = comparedates(possible_dates)
            academic_cluster.update({'from_date': entry_date,
                                       'to_date': exit_date})
        else:
            if possible_dates:
                entry_date = 'unknown'
                exit_date = possible_dates[0]
                academic_cluster.update({'from_date': entry_date,
                                       'to_date': exit_date})

        unique_identifier+=1
        formatted_academics.update({'E{}'.format(unique_identifier):academic_cluster})

    return formatted_academics


def formatExperienceinfo(sent_tokens,sent2idx,alldesignation,
                        allcompany,alldate,alllocations,allroles):


    unique_identifier = 0
    designation_index = []
    company_index = []
    date_index = []
    location_index = []
    role_index = []
    formatted_experience = {}
    item_tracker = {}
    for sentence in sent_tokens:
        cleaned_sentence = cleandata(sentence)
        for designation in alldesignation:
            cleaned_designation = cleandata(designation)
            if cleaned_designation in cleaned_sentence:
                if cleaned_designation not in item_tracker:
                    item_tracker.update({cleaned_designation:1})
                    designation_index.append((designation,sent2idx[cleaned_sentence]))


                elif cleaned_designation in item_tracker:
                    if cleaned_designation == cleaned_sentence:
                        key = cleaned_sentence+'{}'.format(item_tracker[cleaned_designation])

                        designation_index.append((designation,sent2idx[key]))
                    else:
                        designation_index.append((designation,sent2idx[cleaned_sentence]))
                alldesignation.remove(designation)
                break


        for company in allcompany:
            cleaned_company = cleandata(company)
            if cleaned_company in cleaned_sentence:
                if cleaned_company not in item_tracker:
                    company_index.append((company,sent2idx[cleaned_sentence]))
                    item_tracker.update({cleaned_company:1})

                elif cleaned_company in item_tracker:
                    try:
                        key = cleaned_sentence+'{}'.format(item_tracker[cleaned_company])
                        company_index.append((company,sent2idx[key]))
                    except:
                        pass
                allcompany.remove(company)
                break


        for location in alllocations:
            cleaned_location = cleandata(location)
            if cleaned_location in cleaned_sentence:
                if cleaned_location not in item_tracker:
                    location_index.append((location, sent2idx[cleaned_sentence]))
                    item_tracker.update({cleaned_location:1})

                elif cleaned_location in item_tracker:
                    if cleaned_location == cleaned_sentence:
                        key = cleaned_sentence +'{}'.format(item_tracker[cleaned_location])
                        location_index.append((location,sent2idx[key]))
                    else:
                        location_index.append((location,sent2idx[cleaned_sentence]))
                    alllocations.remove(location)

                break


        for role in allroles:
            if role in sentence:
                role_index.append((role,sent2idx[cleaned_sentence]))
                allroles.remove(role)
                break
        checked_date = []
        counter = 0
        for date in alldate:
            if date in sentence:
                found_date = []
                if date.lower()== "present" or date.lower() == "current":
                    if counter == 0:
                        datetime_object = datetime.datetime.now()
                        found_date = [datetime_object]
                        counter += 1
                else:
                    try:
                        found_date = [d for d in datefinder.find_dates(date)]

                    except:

                        pass

                if found_date:
                    formatted_date = found_date[0].strftime("%d-%m-%Y")
                    if (formatted_date, sent2idx[cleaned_sentence]) not in checked_date:
                        date_index.append((formatted_date, sent2idx[cleaned_sentence]))
                        checked_date.append((formatted_date, sent2idx[cleaned_sentence]))
                    else:
                        pass



    for i in range(len(designation_index)-1):
        j = i+1
        if designation_index[i][1] == designation_index[j][1]:
            new_designation = ((designation_index[i][0]+' '+ designation_index[j][0]))
            new_index = designation_index[i][1]
            designation_index.remove((designation_index[i][0],designation_index[i][1]))
            designation_index.remove((designation_index[i][0],designation_index[i][1]))
            designation_index.append((new_designation,new_index))
            designation_index.append(('dummy',1000))

    for i in range(len(company_index)-1):
        j = i+1
        if company_index[i][1] == company_index[j][1]:
            new_company = ((company_index[i][0]+' '+company_index[j][0]))
            new_index = company_index[i][1]
            company_index.remove((company_index[i][0],company_index[i][1]))
            company_index.remove((company_index[i][0],company_index[i][1]))
            company_index.append((new_company,new_index))
            company_index.append(('dummy',100))

    for designation,desigindex in designation_index:
        experience_cluster = {}
        if designation != 'dummy':
            experience_cluster.update({'Designation':designation})
        for company,comindex in company_index:
            if abs(desigindex - comindex) <= 2:
                experience_cluster.update({'company':company})
        for location,locindex  in location_index:
            if abs(desigindex - locindex) <= 2:
                experience_cluster.update({'location':location})
        possible_dates = set()
        for date,dateindex in date_index:
            if abs(desigindex - dateindex ) <= 4 and (date,dateindex) not in possible_dates:
                possible_dates.add((date,dateindex))
                # date_index.remove((date,dateindex))
        j = 0

        possible_dates = list(possible_dates)
        if len(possible_dates)>=2:
            for i in range(len(possible_dates) - 2):
                for j in range(i+1,len(possible_dates)-1):

                    try:
                        if possible_dates[i][1] == possible_dates[j][1] or\
                                abs(int(possible_dates[i][1]) - int(possible_dates[j][1])==1):
                                exit_date,entry_date = comparedates(possible_dates)
                                experience_cluster.update({'entry_date': entry_date,
                                                        'exit_date': exit_date})
                        else:
                            if possible_dates[i][1] > possible_dates[j][1]:
                                date_index.append((possible_dates[i][0], possible_dates[i][1]))
                                possible_dates.remove((possible_dates[i][0], possible_dates[i][1]))

                            else:
                                date_index.append((possible_dates[j][0], possible_dates[j][1]))
                                possible_dates.remove((possible_dates[j][0], possible_dates[j][1]))

                    except:
                        pass

        else:
            if possible_dates:
                entry_date = 'unknown'

                exit_date = possible_dates[0][0]
                experience_cluster.update({'entry_date': entry_date,
                                                    'exit_date': exit_date})


        try:
            experience_cluster.update({'roles':allroles[unique_identifier]})
        except:
            pass
        unique_identifier+=1
        formatted_experience.update({'Exp{}'.format(unique_identifier):experience_cluster})

    return formatted_experience














