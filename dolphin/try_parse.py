import os

import json

from cvparser.newParse import Parser

java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

parser = Parser()
result = parser.identifyResume(r"C:\Users\Aakash\Desktop\Python\Scraping\Projects\dolphin2\seven\dolphin\cvparser\datasets\resumes\Ananya Jain BA Pharma2.docx")
assert(json.dumps(result))
j_result = json.dumps(result)
assert(json.loads(j_result))