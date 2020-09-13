FROM python:3.6
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get --assume-yes install default-jre
RUN apt-get --assume-yes install poppler-utils
RUN apt-get install -y antiword
RUN apt-get update -y
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download en_core_web_md
COPY nltk_download.py ./
RUN python3 nltk_download.py
CMD python ./dolphin/run.py --port 8002
