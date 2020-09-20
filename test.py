import pickle
from sklearn import preprocessing


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

def test_preds(model):

    testSet = pickle.load(open('testSet.pkl','rb'))

    X_test, _ = label_encoding(testSet)

    scaler = pickle.load(open('scaler.pkl','rb'))
    X_test = scaler.transform(X_test)


    preds = model.predict(X_test)
    
    return preds
