import numpy as np
import pandas as pd
from sklearn import preprocessing
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
import pickle


def data_loading():
    global trainingSet, testSet
    train = pd.read_csv(path + '/UNSW_NB15_training-set.csv') #82332 
    test = pd.read_csv(path + '/UNSW_NB15_testing-set.csv') #175341

    cyberattack_data = pd.concat([train, test])
    cyberattack_data.reset_index(drop=True, inplace=True)
    return cyberattack_data

def train_test(cyberattack_data):
    # train:val:test = 0.7:0.2:0.1
    # test만 먼저 분류
    trainingSet, testSet = train_test_split(cyberattack_data, test_size=0.1)
    pickle.dump(testSet, open(path+'/testSet.pkl','wb'))
    return trainingSet


#### preprocessing

"""
예측변수 y를 숫자로 매핑(인코딩)
: 범주형클래스를 numerical로 변환해줌
"""
def label_encoding(cyberattack_data):
    le = preprocessing.LabelEncoder()
    num_cat = le.fit_transform(cyberattack_data.attack_cat) #변환된 attack_cat

    y = num_cat.tolist() # y(true class)
    X = cyberattack_data.drop(columns=['id','attack_cat','label'])

    return X, y

"""
categorical 변수를 dummy value로 변환  
"""
def to_dummies(cyberattack_data_X):
    #categorical_mask = (cyberattack_data_X.dtypes == np.object)
    categorical_mask = ['proto', 'service', 'state']
    list_cat = cyberattack_data_X.loc[:,categorical_mask].columns.tolist()
    X = pd.get_dummies(cyberattack_data_X, columns=list_cat)

    return X
"""
변수간 스케일 조정
: scaler적용해야 인공신경망 적용시 예측이 잘 됨
"""
def value_scale(X_train, X_test):
    scaler = StandardScaler()
    scaler.fit(X_train)

    StandardScaler(copy=True, with_mean=  True, with_std=True)

    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    pickle.dump(scaler, open(path + 'scaler_train.pkl','wb'))
    
    return X_train, X_test
  
 
def classifier(mode, X_train, y_train, X_test, y_test):
    if mode == 'decisiontree':
        clf = DecisionTreeClassifier(random_state=0)
    elif mode == 'randomforest':
        clf = RandomForestClassifier(random_state=0)
    elif mode == 'knn':
        clf = KNeighborsClassifier(5)
    elif mode == 'AdaBoost':
        clf = AdaBoostClassifier()
    elif mode == 'SVC':
        clf = SVC(kernel = 'linear', C = 1)
    elif mode == 'GaussianNB':
        clf = GaussianNB()


    clf.fit(X_train, y_train)
    pickle.dump(clf, open(path+'/'+mode+'model.pkl','wb'))
    preds = clf.predict(X_test)
    model_evalution(clf, y_test, preds)
 

def model_evalution(clf, y_val, preds):
  from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

  print ("Train Accuracy :: ", accuracy_score(y_train, clf.predict(X_train)))
  print ("Validate Accuracy  :: ", accuracy_score(y_val, preds))
  
  from sklearn.metrics import classification_report
  print(classification_report(y_val, preds))

"""
main
"""
cyberattack_data = data_loading()
cyberattack_data = to_dummies(cyberattack_data) # 전체에 대한 더미변수 생성
trainingSet = train_test(cyberattack_data) # 트레인 테스트 쪼갬
X, y = label_encoding(trainingSet) # 트레인 데이터 X,y나눔
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = 0.2, random_state = 42) # train, val데이터 나눔  
#classify
X_train, X_val = value_scale(X_train, X_val)
classifiers = ['decisiontree', 'randomforest', 'knn', 'AdaBoost', 'SVC', 'GaussianNB','Boosting']
classifier(classifiers[0], X_train, y_train, X_val, y_val)
  
  
"""
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
def value_scale(X_train, X_test):
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
    value_scale(X_train, X_test)
    if mode == 'decisiontree':
        clf = DecisionTreeClassifier(random_state=0)
    elif mode == 'randomforest':
        clf = RandomForestClassifier(random_state=0)
    elif mode == 'knn':
        clf = KNeighborsClassifier(5)
    elif mode == 'AdaBoost':
        clf = AdaBoostClassifier()
    elif mode == 'SVC':
        clf = SVC(kernel = 'linear', C = 1)
    elif mode == 'GaussianNB':
        clf = GaussianNB()


    clf.fit(X_train, y_train)
    pickle.dump(clf, open('./testFolder/'+mode+'model.pkl','wb'))
    preds = clf.predict(X_test)
    model_evalution(clf, preds)

def model_evalution(clf, preds):
  from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score

  print ("Train Accuracy :: ", accuracy_score(y_train, clf.predict(X_train)))
  print ("Test Accuracy  :: ", accuracy_score(y_test, preds))
  
  from sklearn.metrics import classification_report
  print(classification_report(y_test, preds))


  
# 분석 main
classifiers = ['decisiontree', 'randomforest', 'knn', 'AdaBoost', 'SVC', 'GaussianNB']
for model in classifiers:
  print("Model is ", model)
  classifier(model)


### 인공신경망 parameter 조정해야함.
clf = MLPClassifier(activation ='relu', hidden_layer_sizes = (30,30,30), alpha = 0.001, max_iter=100)

clf.fit(X_train, y_train)
preds = clf.predict(X_test)
model_evalution(preds)
"""
