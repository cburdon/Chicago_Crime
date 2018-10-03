import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///austin_traffic2.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Data = Base.classes.sensor_data
Detector = Base.classes.traffic_detector
Sensor = Base.classes.travel_sensor

@app.route("/")
def index():
    return render_template("index.html")

""" @app.route("/heatmap")
def heatmap():
    return render_template("map-google.html")

@app.route("/charts")
def charts():
    return render_template("charts.html")

 """
""" @app.route("/sensors")
def sensors():
    Return a list of sample names.

    # Use Pandas to perform the sql query
    stmt = db.session.query(Sensor).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

@app.route("/data")
def data():
    Return a list of sample names.

    # Use Pandas to perform the sql query
    stmt = db.session.query(Data).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])

 """
if __name__ == "__main__":
    app.run()
