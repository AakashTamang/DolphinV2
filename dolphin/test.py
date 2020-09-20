# from datetime import datetime, date

# entry_date = "2018-09-09"
# exit_date = ""

# if not exit_date:
#     exit_date = str(date.today())

# total_exp_days = abs(datetime.strptime(exit_date, "%Y-%m-%d")-datetime.strptime(entry_date, "%Y-%m-%d")).days

# print(total_exp_days)




# coding: utf8
# import spacy
# nlp = spacy.load("en_core_web_sm")

# from spacy.lang.en import English
# nlp = English()

from spacy.lang.ne.stop_words import STOP_WORDS
from spacy.lang.ne import Nepali 
from spacy.lang.ne.examples import sentences

print(len(STOP_WORDS))
nlp = Nepali()

docs = nlp.pipe(sentences)

for doc in docs:
    # assert doc.is_parsed
    tests = [(w.text, w.pos_) for w in doc]

print(tests)
with open("testing.txt", 'w', encoding="utf-8") as f:
    for word in tests:
        f.write(str(word))
    f.close()