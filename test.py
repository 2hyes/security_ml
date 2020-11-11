import pickle
from sklearn.utils import shuffle

"""
웹에서 입력한 날짜의 로그를 샘플링
"""
def daily_log(selected_date):
    testSet = pickle.load(open('testSet.pkl','rb'))
    testSet = shuffle(testSet)
        
    if selected_date == 1:
        return testSet[0:len(testSet) // 5]
    
    elif selected_date == 2:
        return testSet[len(testSet) // 5 : len(testSet) // 5 * 2]
    
    elif selected_date == 3:
        return testSet[len(testSet) // 5 * 2 : len(testSet) // 5 * 3]
    
    elif selected_date == 4:
        return testSet[len(testSet) // 5 * 4 : len(testSet)]

def test_preds(model, selected_date):
    selected_date = int(selected_date)
    testSample = daily_log(selected_date)
    X_test = testSample.drop(columns=['id','attack_cat','label'])
    #X_test, _ = label_encoding(testSample)

    scaler = pickle.load(open('scaler_train.pkl','rb'))
    X_test = scaler.transform(X_test)


    preds = model.predict(X_test)
    
    return preds
