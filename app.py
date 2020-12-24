from flask import Flask,  render_template, request, jsonify
import pickle
import numpy as np
import test
import preds_mapping

app = Flask(__name__)
model = pickle.load(open('.\mlpmodel.pkl', 'rb'))

def getPredictedAttack():
    if request.method == 'POST':
        selected_date = request.form['date']
        preds = test.test_preds(model, selected_date)

        global prediction
        prediction = preds_mapping.attack_category_mapping(preds)

    return prediction


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
    preds_attack = getPredictedAttack()
    return render_template("result.html", result = preds_attack)

@app.route('/entry', methods = ['POST'])
def home():
    data = request.get_json()

    numberOfFields = data.get("numberOfFields")
    result = data.get("result")

    result = prediction

    data = {
        "numberOfFields" : numberOfFields,
        "result" : result
    }
    return jsonify(data)

@app.route('/info')
def info():
    return 'Info'

if __name__ == '__main__':
    app.run(debug = True)
