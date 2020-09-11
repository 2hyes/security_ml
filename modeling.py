import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer
from sklearn import preprocessing
import sklearn
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import pickle

train = pd.read_csv('./data/UNSW_NB15_training-set.csv')

X = train.iloc[:,0:43]
Y = train.iloc[:,43]

## categorical 변수
mask = (train.dtypes == np.object)
list_cat = train.loc[:,mask].columns.tolist()

## 수치형 변수
mask = (train.dtypes != np.object)
list_cat = train.loc[:,mask].columns.tolist()


# sklearn.preprocessing 안의 모듈인 LabelEncoder를 활용해서 
# 범주형클래스를 numerical로 변환해줌
le=preprocessing.LabelEncoder()
num_cat = le.fit_transform(train.attack_cat) #변환된 attack_cat

Y = num_cat.tolist() # Y(true class)
X = train.drop(columns=['id','attack_cat','label'])

## categorical 변수

mask = (X.dtypes == np.object)
list_cat = X.loc[:,mask].columns.tolist()
X = pd.get_dummies(X, columns=list_cat)

#### ML analysis ####
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
clf = DecisionTreeClassifier(random_state=0)
clf.fit(X_train, y_train)
pickle.dump(clf, open('./dtmodel.pkl','wb'))
