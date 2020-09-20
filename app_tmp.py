from flask import Flask,  render_template, request, jsonify
import pickle
import numpy as np
import test_preprocessing
import test_mapping

app = Flask(__name__)
model = pickle.load(open('randomforestmodel.pkl', 'rb'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        i = request.form['log']
        preds = test_preprocessing.test_prediction(model, i)
        preds_attack = test_mapping.attack_category_mapping(preds)
    return render_template("result.html",result = preds_attack)


      #result = request.form #폼 관련데이터 다루는 곳
    
    # 입력받은 여러개의 데이터들을 [np.array]로 저장해서, predict.
    #  test_log = request.form['log']
    #  test_log = test_log.split(',')
    #  test_log = list(map(float, test_log))
    #  preds = model.predict([np.array(test_log)])[0]



@app.route('/info')
def info():
    return 'Info'

if __name__ == '__main__':
    app.run(debug = True)
