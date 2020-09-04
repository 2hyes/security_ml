
from flask import Flask,  render_template, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('dtmodel.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    import numpy as np
    #int_features = [int(x) for x in request.form.values()]
    int_features = request.form.getlist()
    final_features = [np.array(int_features)]
    preds = model.predict(final_features)[0]

    ## mapping 정보
    attack_cat = ['Analysis', 'Backdoor', 'DoS', 'Exploits', 'Fuzzers', 'Generic', 'Normal', 'Reconnaissance', 'Shellcode', 'Worms']

    preds_attack = attack_cat[preds]

    return render_template('index.html', prediction_text='입력된 로그에 대한 attack category는 {}'.format(preds_attack))


@app.route('/results',methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


#@app.route('/post', methods=['POST'])
#def post():
#    data = request.get_json()
#    value = data.get("test")
#    data = {
#        "test": value
#    }
#    print(data)
#    return jsonify(data)# 받아온 데이터를 다시 전송


if __name__ == '__main__':
    app.run(debug = True)
