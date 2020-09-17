import requests
import json
import time

# Azure Endpoint == http://40.122.71.113:8002
# Info server endpoint = http://139.5.71.109:8002
desired_endpoint = "http://0.0.0.0:8002"

# # # # # parsing api test
url_endpoint = desired_endpoint+"/parse"

resume_file = open(
    "/home/shushant/Downloads/Ashish Suwal.docx", "rb")

start_time1 = time.time()
response = requests.post(url_endpoint, files={'resume': resume_file})
print("New API results")
print(response)
print(response.json())
print("Time taken: {} ".format(time.time() - start_time1))

#scoring api for multiple job descriptions
# url_endpoint = desired_endpoint+"/generatescoreprofile"

# with open("multiple_jd.json", 'r') as f:
#     data = json.load(f)

# start_time = time.time()
# response = requests.post(url_endpoint, json=data)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(response.status_code)
# print(response.json())
# print(type(response.json()))


#scoring api for multiple user profiles test
# url_endpoint = desired_endpoint+"/generatescorejobdescription"

# with open("multiple_user_profile.json", 'r') as f:
#     data = json.load(f)

# start_time = time.time()
# response = requests.post(url_endpoint, json=data)
# print("--- %s seconds ---" % (time.time() - start_time))
# print(response.status_code)
# print(response.json())
# print(type(response.json()))


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

# job_desc_1 = """
# QualificationsExperience:US citizenship, 1 year (Required)Education:Bachelor's (Required)Work authorization:United States (Required)Full Job DescriptionDOD client (US Citizenship required)Position SummaryYou will be a software engineer tasked with developing, testing and maintaining a suite of software applications and tools that support our aircraft survivability programs. Your role will require operating as a member of an integrated team alongside other engineering disciplines such as embedded software, systems engineering and product/test engineering.Basic Qualifications and Required SkillsB.S. in Computer Science, Computer Engineering, Software Engineering or a related disciplne from an accredited institution or equivalent combination of education and experience.5+ years of experience in software engineering.Active security clearance or ability to obtain security clearance is requiredExpertise in PythonExpertise in object oriented software developmentExperience developing desktop applications with the .NET Framework, C#, Visual StudioExperience developing desktop applications and/or software libraries with C or C++ is nice to haveExperience with source control repositories such as Git or SVNExperience following an established software engineering processExperience with software build tools such as JenkinsExcellent written and verbal communication skills requiredDuties and ResponsibilitiesResponsible for software engineering tasks including requirements/user story definition, software application and library design, implementation, integration, verification, validation and maintenance.Other duties as assigned.Job Type: ContractPay: $50.00 - $70.00 per hourBenefits:Dental insuranceHealth insuranceSchedule:Monday to FridayCOVID-19 considerations:Due to the nature of the work, candidates must be available to work onsite in a secure area.Experience:US citizenship: 1 year (Required)Education:Bachelor's (Required)Work authorization:United States (Required)Contract Renewal:LikelyFull Time Opportunity:YesCompany's website:www.cornerstonetek.comWork Remotely:Temporarily due to COVID-19If you require alternative methods of application or screening, you must approach the employer directly to request this as Indeed is not responsible for the employer's application process.\n
# """
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
# print(response.json())
# print("Time taken: {} seconds".format(time.time() - start_time1))
