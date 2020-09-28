import time

from doc_classifier_test import DocClassifier
# spacy for lemmatization
import spacy
import pandas as pd

#model path
classifierModelPath = "../models/new_model_svc.pkl"

#load vocabulary from the vectorizer
tfidfModelPath = "../models/tfidf1.pkl"

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

start_time = time.time()

df = pd.read_excel("../datasets/test_data.xlsx")

factor = pd.factorize(df['category'])[0].tolist()

keywords = df['Text']
keywords_list = []
for token in keywords:
    my_string = " "
    a = eval(token)
    keywords_list.append(my_string.join(a))

# Predicted class representation :
#  0 > others
#  1 > resume
#  2 > job_description

result = []
for processed_text in keywords_list:
    docObj = DocClassifier(tfidfModelPath, classifierModelPath, nlp)
    result.append(docObj.classify(processed_text))

data = {"Actual":factor,"predicted":result}
df2 = pd.DataFrame(data)
print(df2)

writer = pd.ExcelWriter('multiTestResult.xlsx', engine='xlsxwriter')

# # Convert the dataframe to an XlsxWriter Excel object.
df2.to_excel(writer, sheet_name='Sheet1')

# # Close the Pandas Excel writer and output the Excel file.
writer.save()

    # print("\nPredicted class representation :\n 0 > others\n 1 > resume\n 2 > job_description\n")
    # print("\nPredicted class : ",result)
    # print("--- %s seconds ---" % (time.time() - start_time))

# print(keywords_list[0])
# exit()
# processed_text = datareader.pdf_to_text('../datasets/testing/Victor-Ekpo.pdf', True)



