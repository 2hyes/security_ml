import numpy as np
import pandas as pd
from sklearn import preprocessing
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pickle

#### data loading
train = pd.read_csv('./data/UNSW_NB15_training-set.csv')
test = pd.read_csv('./data/UNSW_NB15_testing-set.csv')

cyberattack_data = pd.concat([train, test])
cyberattack_data.reset_index(drop=True, inplace=True)

#### preprocessing
# sklearn.preprocessing 안의 모듈인 LabelEncoder를 활용해서 
# 범주형클래스를 numerical로 변환해줌
le = preprocessing.LabelEncoder()
num_cat = le.fit_transform(cyberattack_data.attack_cat) #변환된 attack_cat

y = num_cat.tolist() # Y(true class)
X = cyberattack_data.drop(columns=['id','attack_cat','label'])

# categorical 변수 --> dummy value
categorical_mask = (X.dtypes == np.object)
list_cat = X.loc[:,categorical_mask].columns.tolist()
X = pd.get_dummies(X, columns=list_cat)

# scaler적용해야 인공신경망 적용시 예측이 잘 됨
def value_scale():
  scaler = StandardScaler()
  scaler.fit(X_train)

  StandardScaler(copy=True, with_mean=  True, with_std=True)

  X_train = scaler.transform(X_train)
  X_test = scaler.transform(X_test)


#### ML analysis
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
#clf = DecisionTreeClassifier(random_state=0)
#clf.fit(X_train, y_train)
#pickle.dump(clf, open('./dtmodel.pkl','wb'))

def classifier(mode):
  if mode == 'decisiontree':
    clf = DecisionTreeClassifier(random_state=0)
  elif mode == 'randomforest':
    clf = RandomForestClassifier(random_state=0)
  elif mode == 'knn':
    clf = KNeighborsClassifier(5)
  elif mode == 'AdaBoost':
    clf = AdaBoostClassifier()

  clf.fit(X_train, y_train)
  pickle.dump(clf, open('./'+mode+'model.pkl','wb'))
  preds = clf.predict(X_test)
  model_evalution(preds)

def model_evalution(preds):
  from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

  print ("Train Accuracy :: ", accuracy_score(y_train, clf.predict(X_train)))
  print ("Test Accuracy  :: ", accuracy_score(y_test, preds))
  
  from sklearn.metrics import classification_report
  print(classification_report(y_test, preds))


  
# 분석 main
classifiers = ['decisiontree',  'randomforest', 'knn', 'AdaBoost']
for model in classifiers:
  print("Model is ", model)
  classifier(model)
  
