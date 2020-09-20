from flask import Flask,  render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('.\AdaBoostmodel.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    import numpy as np
    if request.method == 'POST':
      #result = request.form #폼 관련데이터 다루는 곳
    
    # 입력받은 여러개의 데이터들을 [np.array]로 저장해서, predict.
      test_log = request.form['log']
      test_log = test_log.split(',')
      test_log = list(map(float, test_log))
      preds = model.predict([np.array(test_log)])[0]

      ## mapping 정보
      attack_cat = ['Analysis', 'Backdoor', 'DoS', 'Exploits', 'Fuzzers', 'Generic', 'Normal', 'Reconnaissance', 'Shellcode', 'Worms']
      preds_attack = attack_cat[preds]

      #return render_template("result.html",result = result)
    return render_template("result.html",result = preds_attack)

@app.route('/info')
def info():
    return 'Info'

if __name__ == '__main__':
    app.run(debug = True)
