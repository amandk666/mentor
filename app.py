import flask
import os

from flask import Flask, url_for, render_template, request, redirect, session
#from flask_sqlalchemy import SQLAlchemy
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer,CountVectorizer

# Create the application.
app = flask.Flask(__name__)

reviews = pd.read_csv('dataset/property.csv')

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        incData = []
        dur = request.form['deposit']
        day = request.form['monthly_rent']
        age = request.form['room_qty']
        bal = request.form['unit_area']
        pday =request.form['has_elevator']
        pout =request.form['building_floor_count']
        cam = request.form['unit_floor']
        stor =request.form['has_storage_area']
        age = request.form['property_age']
        input = [dur, day, age, bal, pday, pout, cam, stor, age]
        print(input)
        for item in input:
          items = item.split(',')
          incData.extend(items)
        print(incData)
        try:
            data = pd.DataFrame(columns = ['deposit', 'monthly_rent', 'room_qty','unit_area','has_elevator', 'building_floor_count','unit_floor', 'has_storage_area', 'property_age'])
            data.loc[len(data)] = incData
            print(data)
            
            if not data.empty:
                print("here",data)
                print("inside model",data)
                model = pickle.load(open('pickle/mentor.pkl','rb'))
                print("here in model")
                result = model.predict(data)
                
                print(result)
                
                return  render_template('view.html',tables= result, titles = ['prediction'])
               
            else:
                print(data)
                return render_template('invalid.html')

        except:
            print(data)
            return render_template('invalid.html')


if __name__ == '__main__':
    app.debug=True
    
    app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
    #app.run()
    
