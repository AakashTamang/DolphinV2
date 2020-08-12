import os
import json
import __init__
import logging
from flask import Flask, request,jsonify
from flask_cors import CORS
from datareader import prepare_text,prepare_text_from_string
from cvparser.newParse import Parser as newParser
from settings import tempStorage

java_path = r"C:\Program Files\Java\jdk-12.0.1\bin\java.exe"
os.environ['JAVAHOME'] = java_path

app = Flask(__name__)
CORS(app, headers="X-CSRFToken, Content-Type")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

new_resume_parser_obj = newParser()

@app.route("/newparse",methods=["POST"])
def new_parse_cv():
    resume = request.files.get('resume')
    if resume:
        filename = resume.filename
        file = tempStorage + '/' + filename
        resume.save(file)
        parsed_user_data = new_resume_parser_obj.identifyResume(file)
        parsed_user_data = json.dumps(parsed_user_data)
        return jsonify(parsed_user_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)
