Introduction to Dolphin
************
---
# dolphin

Dolphin is the **Dolphwin**'s Artificial Intelligence component -- as intelligent as a Dolphin.

# Directory Structure

    └── dolphwin                      # Main Directory

        ├── dolphin                       # AI package for Dolphwin

                ├── archives

                ├── data                # data for pool parsing

                    ├── languages.csv           # predefined pool for languages

                    ├── nationality_data.csv    # predefined pool for nationalities

                    ├── soft_skills_resume.csv  # predefined pool for soft skills

                    ├── technical_skills.csv    # predefined pool for technical skills

                ├── datasets               # data of resume, job description and other files

                ├── docs                   # 📄 project document files

                ├── labs                   # 🔬 contains research program files

                ├── models                 # machine learning models saved

                    ├── NER_model.ser.gz   # NER model saved from training with Stanford NLP

                    ├── stanford_ner.jar   # pretrained stanford model

                    ├── segment_identifier.pkl  # model trained for resume segmentation

                    ├── new_model_svc.pkl   # SVC model for document classification

                    ├── tfidf1.pkl          # tfidf model used for document classification

                ├── segmentation            # module for resume segmentation

                    ├── segment_resume.py   # python module for resume segmentation

                ├── stanfordNER             # module for parsing using NER

                    ├── formatdata.py       # module for formatting data

                    ├── namedentityrecognition.py   # module for getting named entities

                    ├── standardizedata.py          # module for standardizing data

                ├── datareader.py           # python module for reading textual content frommultiple extension files

                ├── pipeline.py             # python module for mantaining every task in custom spacy pipeline

                ├── evaluate_pipeline.py    # python module for testing working of pipeline with a test resume

                ├── settings.py              # python module for mantaining configurations

                ├── settings.json            # configuration in json format

        ├── tests                         # all unit testing files

            ├── test_datareader.py              # unit testing file for datareader module

            ├── test_identify_resume.py         # unit testing file for document categorization module

            ├── test_ner_parsing.py             # unit testing file for testing ner parsing module

            ├── test_segment_resume.py          # unit testing file for testing resume segmentation module

        ├── setup.py                      # setup file for pip

        ├── LICENSE                       # License details

        ├── info.log                      # Logs mantained using logging module

        ├── requirements.txt              # list of python modules required to run the system

        ├── README.md                     # markdown documentation of the system

---

# Pipelines

The pipelines used in this system are shown in the below diagram.
![pipeline](pipeline.png)

## Document Categorization pipeline

This is a custom spacy pipeline which is used for identifying the category of any textual documents. The input documents supports following file formats:

- .pdf
- .docx
- .doc
- .txt

The cateogory defined in the pipeline are as follows:

1. Resume
2. Job Decription
3. Others

This pipeline is developed training a Support Vector Classifier with training data containing 400 samples each of resume, job descriptions and other files.

> Trained model for document categorization -----> new_model_svc.pkl

### Usage

```
from pipeline import nlp

doc = nlp(textual_content_of_file)

category = doc._.category

```

## Segmentation pipeline

This pipeline is used to segment any resume to following segments:

- Profile segment
- Objective segment
- SKills segment
- Academics segment
- Experience segment
- Language segment
- Projects segment
- Rewards segment
- References segment
- Links segment

If any document is categorized as resume, it is passed to the segmentation pipeline to break down into different resume segments.

> Trained model for resume segmentation --> segment_identifier.pkl

### Usage

```
from pipeline import nlp

doc = nlp(textual_content_of_file)

profile_segment = doc._.profile_segment
objective_segment = doc._.objective_segment
skills_segment = doc._.skills_segment
academics_segment = doc._.academics_segment
experience_segment = doc._.experience_segment
language_segment = doc._.language_segment
projects_segment = doc._.projects_segment
rewards_segment = doc._.rewards_segment
references_segment = doc._.references_segmen
links_segment = doc._.links_segment
```

## NER Parser pipeline

This pipeline is developed for the extraction of vital informations from any resume such as experience, education, personal information with name and address from any resume. For extractoin of such information from any resume, custom **Named Entity Recognition(NER)** model has been trained. This model has been trained using the **StanfordNLP** NER training interface. This model has been trained with the tokens of about 285 resumes.

The information extraction from resume using this pipeline are as follows:

- Name
- Address
- Education
- Experience

> Trained model for Named Entity Recognition ----> NER_model.ser.gz

### Usage

```
from pipeline import nlp

doc = nlp(textual_content_of_the_file)
name = doc._.name
address = doc._.address
experience = doc._.experience
education = doc._.education
```

## Pattern Matching Pipeline

The information which follows a specific pattern or is contained with finite pool have been extracted using Spacy Matcher. The information extracted using this pipelines are as follows:

- technical skills
- soft skills
- nationality
- languages
- date
- phone number
- gender
- email

### Usage

```
from pipeline import nlp
doc = nlp(textual_content_of_file)

nationality = doc._.nationality
language = doc._.language
email = doc._.email
phone_number = doc._.phone
technical_skills = doc._.technical_skills
soft_skills = doc._.soft_skills
date = doc._.date
gender = doc._.gender
```

# Modules Used

- PyMuPDF
- texteract
- datefinder
- docx2xt
- gensim
- nltk
- spacy
- pytesseract
- sklearn

> Other requirement ---> Downloading en_core_web_sm modle from spacy ----> python -m spacy download en_core_web_sm
