import requests
import json
import time

# parsing api test

# server_url_endpoint = "http://139.5.71.109:8002/parse"
# local_url_endpoint = "http://0.0.0.0:8004/parse"

# resume_file = open(
#     "/home/shushant/Desktop/Data_dump/data_resume/Akhil_Devops.docx", "rb")

# start_time1 = time.time()
# response = requests.post(local_url_endpoint, files={'resume': resume_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} ".format(time.time() - start_time1))

# start_time2 = time.time()
# response2 = requests.post(server_url_endpoint, files={'resume': resume_file})
# print("Server API results")
# print(response2)
# print(response2.json())
# print("Time taken: {} ".format(time.time() - start_time2))


# scoring api for multiple job descriptions
# scoring_multiple_jd_endpoint = "http://0.0.0.0:8004/scoreresume"

# with open("multiple_jd.json", 'r') as f:
#     data = json.load(f)

"""
"""
# # scoring api for multiple user profiles test
# scoring_multiple_user_profile_endpoint = "http://0.0.0.0:8004/generatescorejobdescription"

# with open("multiple_user_profile.json", 'r') as f:
#     data = json.load(f)

# start_time = time.time()
# response = requests.post(scoring_multiple_jd_endpoint, json=data)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(response.status_code)
# print(response.json())
# print(type(response.json()))


# parsing job description test
# local_url_endpoint = "http://0.0.0.0:8002/parsejd"

# jd_file = open(
#     "/home/shushant/Desktop/Data_dump/Job Description Collection/Python Developer 10.docx", "rb")

# start_time1 = time.time()
# response = requests.post(local_url_endpoint, files={'job_description': jd_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} seconds".format(time.time() - start_time1))

# domain classification test

# local_url_endpoint = "http://0.0.0.0:8002/domainclassification"

# jd_file = open(
#     "/home/shushant/Desktop/Data_dump/Job Description Collection/Python Developer 10.docx", "rb")

# start_time1 = time.time()
# response = requests.post(local_url_endpoint, files={'job_description': jd_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} seconds".format(time.time() - start_time1))
"""
# scoring from jd and resume content word2vec test
local_url_endpoint = "http://0.0.0.0:8002/generatescore"

resume_file = open(
    "/home/shushant/Desktop/Data_dump/data_resume/Akhil_Devops.docx", "rb")

jobs = [{'pk':2, 'job_description': 'we are looking for python dev'}, {'pk':3, 'job_description':'looking for java dev'}]

start_time1 = time.time()
response = requests.post(local_url_endpoint, files={'resume': resume_file} , data = {'jobs':jobs})
print("New API results")
print(response)
print(response.json())
print("Time taken: {} seconds".format(time.time() - start_time1))
"""
