from flask import Flask, render_template, url_for, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
import queries
import sqlite3
import pandas as pd
import pickle

import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer.db'
db = SQLAlchemy(app)

class customers(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    Age = db.Column(db.Integer)

    def __repr__(self):
        return '<Task %r>' % self.ID

result = {}

def get_by_Name(Name):
    conn = sqlite3.connect('customer.db')
    cur = conn.cursor()
    statement = "SELECT * FROM customers WHERE Name = ?"
    cur.execute(statement, [Name])
    cust_details = cur.fetchall()
    return cust_details

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
    tasks = customers.query.limit(5).all()
    return render_template('index.html', tasks=tasks)

@app.route("/Name", methods = ["GET"])
def get_cust():
    global sent_global
    body = request.args.get('Name')
    sent = get_by_Name(body)
    sent_global = get_by_Name(body)
    sent_global = [list(l) for l in sent_global]
    print(sent_global)
    return render_template('update.html', sent=sent)
    

@app.route("/Predict", methods = ["GET"])
def age_predict():
    body = request.args.get('Predict')
    df = pd.DataFrame(sent_global)
    df = pd.get_dummies(df)
    
    df['new'] = 0  # have to remove it
    print(df)
    sent_predict = predict(df)
    print(sent_predict)
    return render_template('update.html', sent_predict=sent_predict)

if __name__ == "__main__":
    app.run(host='127.0.0.13', port=8080, debug=True)
