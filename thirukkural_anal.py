# -*- coding: utf-8 -*-
"""Thirukkural_anal.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qK-jT0yCPUyLgGfzkVg2I4hu42_STjRH
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("/content/drive/MyDrive/thirukkural analysis/data/Thirukural.csv")

df.head()

"""# Imports

"""

from sklearn.preprocessing import OneHotEncoder,LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans,kmeans_plusplus,AgglomerativeClustering
from sklearn.svm import SVC
from scipy.stats import chi2_contingency
from collections import Counter
from scipy.stats import entropy
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay,classification_report

"""# Analysis


SO let us start with the basics. (I know these as I've read this)
"""

df['Chapter Name'].value_counts()

"""#### Translation vs Original

Let us apply same transformers and learn with the same set of learners on both and see do they really perform similar

Let us <strong>split</strong> the data
"""

X,y=df[['Verse','Translation']],df['Chapter Name']

ct_eng=ColumnTransformer([
    ('Eng',OneHotEncoder(),['Translation'])
])
ct_tam=ColumnTransformer([
    ('Tam',OneHotEncoder(),['Verse'])
])

X_eng=ct_eng.fit_transform(X)
X_tam=ct_tam.fit_transform(X)

X_train,X_test,y_train,y_test=train_test_split(X_eng,y,test_size=0.3,random_state=42)

mlp_eng=MLPClassifier(hidden_layer_sizes=(10,15),alpha=5)

mlp_eng.fit(X_train,y_train)

print("Train for English: ",mlp_eng.score(X_train,y_train))
print("Train for English: ",mlp_eng.score(X_test,y_test))

X_train,X_test,y_train,y_test=train_test_split(X_tam,y,test_size=0.3,random_state=42)

mlp_tam=MLPClassifier(hidden_layer_sizes=(10,15),alpha=4)

mlp_tam.fit(X_train,y_train)

print("Train for English: ",mlp_tam.score(X_train,y_train))
print("Train for English: ",mlp_tam.score(X_test,y_test))

np.not_equal(X_tam.toarray(),X_eng.toarray())

X_tam.toarray().shape, X_eng.toarray().shape

"""### Let us try clustering huh?!"""

km=AgglomerativeClustering(n_clusters=3,linkage='average')

km.fit(X_eng.toarray())

y_eng=km.fit_predict(X_eng.toarray())

X_train,X_test,y_train,y_test=train_test_split(X_eng,y_eng,test_size=0.3,random_state=42)

svm=SVC()

svm.fit(X_train,y_train)

svm.score(X_train,y_train)

svm.score(X_test,y_test)

pd.Series(y_eng).value_counts()

df['Chapter Name'].value_counts()

print(list(df['Chapter Name']))

print(list(y_eng))

"""அறத்துப்பால் = 0
பொருட்பால் =2
காமத்துப்பால் =1

### Let's do this with Tamil
"""

km_tam=AgglomerativeClustering(n_clusters=3,linkage='average')

y_tam=km_tam.fit_predict(X_tam.toarray())

X_train,X_test,y_train,y_test=train_test_split(X_tam,y_tam,test_size=0.3,random_state=42)

svm.fit(X_train,y_train)
print(svm.score(X_train,y_train))
svm.score(X_test,y_test)

pd.Series(y_tam).value_counts()

"""Funny how the clustering seems too similar?!?!?

## Trying other models

### Cramer's V measure
"""

confusion_matrix = pd.crosstab(df['Verse'],df['Translation'])
chi2 = chi2_contingency(confusion_matrix)[0]
n = confusion_matrix.sum().sum()
r, k = confusion_matrix.shape
print(np.sqrt(chi2 / (n * (min(r, k) - 1))))

"""### Thiel's U"""

px = Counter(df['Verse'])
py = Counter(df['Translation'])
pxy = Counter(zip(df['Verse'], df['Translation']))
hx = entropy(list(px.values()), base=2)
hxy = entropy(list(pxy.values()), base=2)
print((hx - hxy) / hx)

"""### Chi-2 **bold text**"""

confusion_matrix = pd.crosstab(df['Verse'],df['Translation'])
chi2, p, _, _ = chi2_contingency(confusion_matrix)
print(p)

"""# Transformers"""

!pip install sentence-transformers

from sentence_transformers import SentenceTransformer, util

trf = SentenceTransformer('distiluse-base-multilingual-cased-v2')

embeddings_Tam = trf.encode(df['Verse'].tolist(), convert_to_tensor=False)
embeddings_english = trf.encode(df['Translation'].tolist(), convert_to_tensor=False)

cosine_similarities = util.pytorch_cos_sim(embeddings_Tam, embeddings_english).diagonal()

sim=cosine_similarities.cpu().numpy()

max(sim),min(sim)

"""Ho Ho! That's quite somethin"""

km=AgglomerativeClustering(n_clusters=3)

y_eng=km.fit_predict(embeddings_english)

y_tam=km.fit_predict(embeddings_Tam)

pd.Series(y_eng).value_counts()

df['Chapter Name'].value_counts()

pd.Series(y_tam).value_counts()

cm=confusion_matrix(LabelEncoder().fit_transform(df['Chapter Name']),y_tam)

cd=ConfusionMatrixDisplay(cm)
cd.plot();

cm=confusion_matrix(LabelEncoder().fit_transform(df['Chapter Name']),y_eng)

cd=ConfusionMatrixDisplay(cm)
cd.plot();

"""I really don't have the slightest reason on this behaviour, guess English is a bit better"""

X_eng,y=embeddings_english,df['Chapter Name']
X_tam,y=embeddings_Tam,df['Chapter Name']

X_eng_train,X_eng_test,y_eng_train,y_eng_test=train_test_split(X_eng,y,test_size=0.3,random_state=42)
X_tam_train,X_tam_test,y_tam_train,y_tam_test=train_test_split(X_tam,y,test_size=0.3,random_state=42)

nn=MLPClassifier(hidden_layer_sizes=(10,15),max_iter=600,alpha=3,activation='relu')

nn.fit(X_eng_train,y_eng_train)

print(classification_report(y_eng_train,nn.predict(X_eng_train)))

print(classification_report(y_eng_test,nn.predict(X_eng_test)))

nn_tam=MLPClassifier(hidden_layer_sizes=(10,15),max_iter=500)

nn_tam.fit(X_tam_train,y_tam_train)

print(classification_report(y_tam_train,nn_tam.predict(X_tam_train)))

print(classification_report(y_tam_test,nn_tam.predict(X_tam_test)))

lr_tam=LogisticRegression(max_iter=1000,C=0.01)

lr_tam.fit(X_tam_train,y_tam_train)

lr_tam.score(X_tam_train,y_tam_train)

lr_tam.score(X_tam_test,y_tam_test)

nb_tam=GaussianNB()

nb_tam.fit(X_tam_train,y_tam_train)

nb_tam.score(X_tam_train,y_tam_train)

nb_tam.score(X_tam_test,y_tam_test)