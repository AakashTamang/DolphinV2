import pdb
import requests
import json
import time

# parsing api test
"""
server_url_endpoint = "http://139.5.71.109:8002/parse"
local_url_endpoint = "http://0.0.0.0:8002/newparse"

resume_file = open(
    "/home/shushant/Desktop/data_resume/VARUN MURDULA_.Net Developer.docx", "rb")

start_time1 = time.time()
response = requests.post(local_url_endpoint, files={'resume': resume_file})
print("New API results")
print(response)
print(response.json())
print("Time taken: {} ".format(time.time() - start_time1))

# start_time2 = time.time()
# response2 = requests.post(server_url_endpoint, files={'resume': resume_file})
# print("Server API results")
# print(response2)
# print(response2.json())
# print("Time taken: {} ".format(time.time() - start_time2))
"""
# scoring api for multiple user profiles test
scoring_multiple_user_profile_endpoint = "http://0.0.0.0:8002/scorejobdes"

with open("multiple_user_profile.json", 'r') as f:
    data = json.load(f)


pdb.set_trace()
start_time = time.time()
response = requests.post(scoring_multiple_user_profile_endpoint, json=data)
print("--- %s seconds ---" % (time.time() - start_time))
print(response.status_code)
print(response.json())
print(type(response.json()))
