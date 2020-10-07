import requests
import json
import time

# Azure Endpoint == http://40.122.71.113:8002
# Info server endpoint = http://139.5.71.109:8002
# desired_endpoint = "http://0.0.0.0:8002"
desired_endpoint = "http://139.5.71.109:8002"

# # # # # # # # # parsing api test
# url_endpoint = desired_endpoint+"/parse"

# resume_file = open(
#     "/home/shushant/Downloads/Ashish Suwal.docx", "rb")

# start_time1 = time.time()
# response = requests.post(url_endpoint, files={'resume': resume_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} ".format(time.time() - start_time1))

# #scoring api for multiple job descriptions
# url_endpoint = desired_endpoint+"/generatescoreprofile"

# with open("multiple_job_v_single_user_profile.json", 'r') as f:
#     data = json.load(f)

# start_time = time.time()
# response = requests.post(url_endpoint, json=data)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(response.status_code)
# print(response.json())
# print(type(response.json()))


# # scoring api for multiple user profiles test
url_endpoint = desired_endpoint+"/generatescorejobdescription"

with open("multiple_user_profile.json", 'r') as f:
    data = json.load(f)

start_time = time.time()
response = requests.post(url_endpoint, json=data)
print("--- %s seconds ---" % (time.time() - start_time))
print(response.status_code)
print(response.json())
print(type(response.json()))
print("Time taken: {} seconds".format(time.time() - start_time))


# # parsing job description test
# url_endpoint =  desired_endpoint+"/parsejd"

# jd_file = open(
#     "/home/shushant/Desktop/jd_sample.txt", "rb")

# start_time1 = time.time()
# response = requests.post(url_endpoint, files={'job_description': jd_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} seconds".format(time.time() - start_time1))

# domain classification test

# local_url_endpoint = "http://0.0.0.0:8002/domainclassification"

# jd_file = open(
#     "/home/shushant/Desktop/Data_dump/jd_collection_3/jd3.txt", "rb")

# start_time1 = time.time()
# response = requests.post(local_url_endpoint, files={'job_description': jd_file})
# print("New API results")
# print(response)
# print(response.json())
# print("Time taken: {} seconds".format(time.time() - start_time1))


# scoring from jd and resume content word2vec test
# url_endpoint = desired_endpoint + "/generatescore"
# resume_file = open(
#     "cvparser/datasets/resumes/Ashish Suwal_Sr. Data Analyst.docx", "rb")


# job_data = [
#     {
#         "pk": 46,
#         "job_description": "Experience in Python , Postgresql , XML , HTML , CSS , JavaScript , JQuery. Experience with common python libraries / frameworks like Django, Flask, Pyramid, Werkzeug Solid understanding of object-oriented programming Familiarity with concepts of MVT, ORM RESTful Knowledge in React JS/Angular JS will be an added advantage Proficient understanding of GIT Able to implement automated testing platforms and unit tests Good Communication in the English language is a must. Knowlege of docker, pandas, pytorch, scikitlearn, numpy, deep learning etc."
#     },
#     {
#         "pk": 103,
#         "job_description": "Set up and manage our AI development and production infrastructure Help AI product managers and business stakeholders understand the potential and limitations of AI when planning new products. Build data ingest and data transformation infrastructure.Identify transfer learning opportunities and new training datasets. Build AI models from scratch and help product managers and stakeholders understand results. Deploy AI models into production.Create APIs and help business customers put results of your AI models into operations.Keep current of latest AI research relevant to our business domain."
#     },
#     {
#         "pk": 42,
#         "job_description": "Experience in Python , Postgresql , XML , HTML , CSS , JavaScript , JQuery. Experience with common python libraries / frameworks like Django, Flask, Pyramid, Werkzeug Solid understanding of object-oriented programming Familiarity with concepts of MVT, ORM RESTful Knowledge in React JS/Angular JS will be an added advantage Proficient understanding of GIT Able to implement automated testing platforms and unit tests Good Communication in the English language is a must. Knowlege of docker, pandas, pytorch, scikitlearn, numpy, deep learning etc."
#     }
# ]

# start_time1 = time.time()
# response = requests.post(url_endpoint,data = {'jobs':job_data},files ={'resume': resume_file})
# print(response.json())
# print(response)
# print("Time taken: {} seconds".format(time.time() - start_time1))


#testing similar job scoring endpoint
# url_endpoint = desired_endpoint + "/getjobscore"
# primary_job = {'pk':2, 'job_title':'Python Developer','job_description': 'we are looking for python dev'}
# other_jobs = [{'pk':2, 'job_title':'Python Developer','job_description': 'we are looking for python dev'}, {'pk':3,'job_title':'Java Developer', 'job_description':'We need java expert'},{'pk':9, 'job_title':'Python Developer','job_description': 'we are looking for java developers'},{'pk':8, 'job_title':'Python Developer','job_description': 'we are looking for python developerss'},{'pk':22, 'job_title':'Python Developer','job_description': 'we are looking for data scientist'}]
# data_to_send = {"primary_job":primary_job,"other_jobs":other_jobs}
# start_time1 = time.time()
# response = requests.post(url_endpoint,json =data_to_send)
# print(response.json())
# print(response)
# print("Time taken: {} seconds".format(time.time() - start_time1))
