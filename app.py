import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

from keras.models import load_model

from form_data.py import *

app = Flask(__name__, static_url_path='/static', static_folder='C:/Users/cburd/Chicago_Crime/crime/static')


#################################################
# Database Setup
#################################################

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C://Users/cburd/Chicago_Crime/crime/datasets/Crime2.sqlite'
# db = SQLAlchemy(app)
# Base = automap_base()
# engine = create_engine(app)
# Base.prepare(engine, reflect=True)


# # reflect the tables
# Base.prepare(db.engine, reflect=True)

# # Save references to each table
# Crime = Base.classes.crime


@app.route("/")
def home():
    """Return the homepage."""
    return render_template("index.html")

@app.route("/crimes_per_year")
def crimes_per_year():
    return render_template("crimes_per_year.html")

@app.route("/frequent_crimes")
def freguent_crimes():
    """Return the homepage."""
    return render_template("frequent_crimes.html")

@app.route("/month_crimes")
def month_crimes():
    """Return the homepage."""
    return render_template("month_crimes.html")

 
@app.route("/top_five")
def top_crimes():
    """Return a list of sample names."""
    return render_template("top_five.html")

try:
    Crime_model = load_model("Cha_Crime_Onehot.h5")
except:
    function_return = "Error with loading the model into Flask."

@app.route("/MLform")
def index(location_list=location_list,hours=hours,crime_type=crime_type,beat=beat):
    return render_template("MLform.html",location_list=location_list,hours=hours,crime_type=crime_type,beat=beat)

@app.route("/ML",methods=['POST'])
def ML():
    form_data = request.form
    ML_predict = np.random.choice(["True","False"], p=[0.3,0.7])
    ML_results = np.random.random()
    data = [form_data, {"Result": ML_predict, "Probability": ML_results}]
    return jsonify(data)
    
# @app.route("/data")
# def names():
#     """Return a list of sample names."""

#     # Use Pandas to perform the sql query
#     stmt = db.session.query(Data).statement
#     df = pd.read_sql_query(stmt, db.session.bind)

#     # Return a list of the column names (sample names)
#     return jsonify(list(df.columns)[2:])


if __name__ == "__main__":
    app.run()
