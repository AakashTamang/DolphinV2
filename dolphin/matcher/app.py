import os
import ast
import json
import concurrent.futures
from flask import Flask, request, jsonify
from flask_cors import CORS
# from settings import tempStorage
from match import matcher

app = Flask(__name__)
CORS(app, headers="X-CSRFToken, Content-Type")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/matcher",methods = ["POST","GET"])
def oneResMultipleJD():
    form_data_ = request.get_json()
    oneJD_MultipleRes_Score = form_data_.get('oneJD_MultipleRes_Score')
    oneRes_MultipleJD_Score = form_data_.get('oneRes_MultipleJD_Score')

    hiredobj = matcher(oneJD_MultipleRes_Score, oneRes_MultipleJD_Score)
    hired = hiredobj.matchmaker()
    result = {"results":['  ' + ',\n  '.join('%s is hired by %s' % match for match in sorted(hired.items()))]}
    return result

@app.route("/",methods=['GET'])
def check_site():
    return ('Matching api is live! Thank you')

if __name__ == "__main__":
    app.run(host='127.0.0.3', port=8003, debug=True)