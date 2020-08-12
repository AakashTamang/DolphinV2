# import os

# import json

# from cvparser.newParse import Parser


# parser = Parser()
# result = parser.identifyResume(
#     r"/home/shushant/Desktop/data_resume/Adithya_JAVA (3).docx")
# j_result = json.dumps(result)

import requests
import time
server_url_endpoint = "http://139.5.71.109:8002/parse"
local_url_endpoint = "http://0.0.0.0:8001/newparse"

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
