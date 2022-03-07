from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import queries
import sqlite3
import pandas as pd
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
db = SQLAlchemy(app)

class students(db.Model):
    class_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.Integer)
    age = db.Column(db.Integer)
    marks = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.class_no

result = {}

def get_by_class(class_no):
    conn = sqlite3.connect('student.db')
    cur = conn.cursor()
    statement = "SELECT * FROM student_marks WHERE class_no = ?"
    cur.execute(statement, [class_no])
    student_details = cur.fetchall()
    return student_details

def predict(body):
    # body = body.split(",")
    # body = [float(i) for i in body]

    # df = pd.DataFrame([body])

    filename = 'linear_regression_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    Y_pred_lr = loaded_model.predict(body)

    return Y_pred_lr

@app.route("/")
def index():
    # tasks = customers.query.limit(5).all()
    return render_template('index.html')

@app.route("/class_no", methods = ["GET"])
def get_student():
    global sent_global
    body = request.args.get('class_no')
    sent = get_by_class(body)
    # print(sent)
    sent_global = get_by_class(body)
    sent_global = [list(l) for l in sent_global]
    # print(sent_global)
    return render_template('update.html', sent=sent)
    

@app.route("/predict", methods = ["GET"])
def marks_predict():
    global df1_global
    body = request.args.get('predict')
    df = pd.DataFrame(sent_global, columns = ['class_no', 'name', 'gender','age','marks'])
    # print(df)
    df1 = pd.DataFrame(sent_global, columns = ['class_no', 'name', 'gender','age','marks'])
    df = df.drop('name', axis=1)
    df = df.drop('marks', axis=1)
    df1 = df1.drop('marks', axis=1)

    sent_predict = predict(df)
    print("-s-s-s-s-s-s-s-s-sw-ws-s-")
    sent_predict =  list(sent_predict)
    df1['marks'] = sent_predict

    df1_global = df1

    return render_template('predict.html',  tables=[df1.to_html(classes='data')], titles=df1.columns.values)

@app.route("/visualize", methods = ["GET"])
def marks_visualization():
    body = request.args.get('visualize')
    
    df1_global['total'] = 100
    df1_global.drop(columns = ['class_no', 'name', 'age', 'gender'], inplace = True)
    print(df1_global)
    # for ind in df1_global.index:
    #     return render_template('visualize.html', fig=df1_global.iloc[ind].plot(kind='pie'))


if __name__ == "__main__":
    app.run(host='127.0.0.13', port=8080, debug=True)
