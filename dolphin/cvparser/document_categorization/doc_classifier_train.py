#Importing Libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
from sklearn import metrics
from sklearn.svm import SVC
import pickle

# df = pd.read_excel("../datasets/data_version_3.xlsx")
df = pd.read_excel("../datasets/train_data.xlsx")
# df[~df.Text.str.contains("")]
df = df[df.Text != '[]']

df['Text'].replace('', np.nan, inplace=True)

df.dropna(subset=['Text'], inplace=True)

df['category'].replace('', np.nan, inplace=True)

df.dropna(subset=['category'], inplace=True)

#Creating the dependent variable class
factor = pd.factorize(df['category'])
df.category = factor[0]
definitions = factor[1]

keywords = df['Text']
keywords_list = []
for token in keywords:
    my_string = " "
    a = eval(token)
    keywords_list.append(my_string.join(a))

category = list(df['category'])

X_train, X_test, y_train, y_test = train_test_split(keywords_list, category, test_size = 0.25, random_state = 65)

# converting text to numerical representation
vectorizer = TfidfVectorizer()
# vectorizer = CountVectorizer()
X_vector = vectorizer.fit(X_train)
X = vectorizer.transform(X_train)
Xt = vectorizer.transform(X_test)

# dump the file
pickle.dump(X_vector, open("../models/tfidf1.pkl", "wb"))
# pickle.dump(X_vector, open("../models/bow.pkl", "wb"))

#  Build your classifier
classifier = SVC()

# Train it on the entire training data set
classifier.fit(X, y_train)

# Get predictions on the test set
y_pred = classifier.predict(Xt)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

#Reverse factorize (converting y_pred from 0s,1s and 2s to other, resume and job descriptions
reversefactor = dict(zip(range(3),definitions))
y_test = np.vectorize(reversefactor.get)(y_test)
y_pred = np.vectorize(reversefactor.get)(y_pred)
# Making the Confusion Matrix
print(pd.crosstab(y_test, y_pred, rownames=['Actual Class'], colnames=['Predicted Class']))

# # Save to file in the current working directory
pkl_filename = "../models/new_model_svc.pkl"
# # pkl_filename = "../models/bow_model_svc.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier, file)

# Load from file
# with open(pkl_filename, 'rb') as file:
#     pickle_model = pickle.load(file)