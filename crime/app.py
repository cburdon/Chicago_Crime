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

# from form_data import *

app = Flask(__name__, static_url_path='/static', static_folder='C:/Users/cburd/Chicago_Crime/crime/static')


# Form_data setup

location_list = ['STREET', 'RESIDENCE', 'APARTMENT', 'SIDEWALK', 'OTHER',
       'PARKING LOT/GARAGE(NON.RESID.)', 'ALLEY', 'SCHOOL, PUBLIC, BUILDING',
       'SMALL RETAIL STORE', 'RESIDENCE-GARAGE', 'RESTAURANT',
       'RESIDENCE PORCH/HALLWAY', 'VEHICLE NON-COMMERCIAL', 'DEPARTMENT STORE',
       'GROCERY FOOD STORE', 'RESIDENTIAL YARD (FRONT/BACK)', 'GAS STATION',
       'PARK PROPERTY', 'CHA PARKING LOT/GROUNDS',
       'COMMERCIAL / BUSINESS OFFICE', 'BAR OR TAVERN', 'CHA APARTMENT',
       'CTA PLATFORM', 'DRUG STORE', 'HOTEL/MOTEL', 'SCHOOL, PUBLIC, GROUNDS',
       'CTA TRAIN', 'BANK', 'CONVENIENCE STORE', 'HOSPITAL BUILDING/GROUNDS',
       'VACANT LOT/LAND', 'CTA BUS', 'CHA HALLWAY/STAIRWELL/ELEVATOR',
       'TAVERN/LIQUOR STORE', 'DRIVEWAY - RESIDENTIAL',
       'POLICE FACILITY/VEH PARKING LOT', 'NURSING HOME/RETIREMENT HOME',
       'CHURCH/SYNAGOGUE/PLACE OF WORSHIP', 'GOVERNMENT BUILDING/PROPERTY',
       'SCHOOL, PRIVATE, BUILDING', 'AIRPORT/AIRCRAFT', 'CONSTRUCTION SITE',
       'ABANDONED BUILDING', 'CURRENCY EXCHANGE', 'ATHLETIC CLUB',
       'CTA STATION', 'WAREHOUSE', 'ATM (AUTOMATIC TELLER MACHINE)', 'TAXICAB',
       'CTA GARAGE / OTHER PROPERTY', 'CTA BUS STOP', 'BARBERSHOP',
       'MEDICAL/DENTAL OFFICE', 'FACTORY/MANUFACTURING BUILDING', 'LIBRARY',
       'SPORTS ARENA/STADIUM', 'VEHICLE-COMMERCIAL',
       'OTHER RAILROAD PROP / TRAIN DEPOT', 'COLLEGE/UNIVERSITY GROUNDS',
       'SCHOOL, PRIVATE, GROUNDS', 'CLEANING STORE',
       'AIRPORT TERMINAL UPPER LEVEL - SECURE AREA', 'DAY CARE CENTER',
       'OTHER COMMERCIAL TRANSPORTATION', 'CAR WASH', 'MOVIE HOUSE/THEATER',
       'AIRPORT TERMINAL LOWER LEVEL - NON-SECURE AREA', 'APPLIANCE STORE',
       'JAIL / LOCK-UP FACILITY', 'AIRPORT VENDING ESTABLISHMENT',
       'LAKEFRONT/WATERFRONT/RIVERBANK', 'COLLEGE/UNIVERSITY RESIDENCE HALL',
       'AIRPORT BUILDING NON-TERMINAL - NON-SECURE AREA', 'HIGHWAY/EXPRESSWAY',
       'AIRPORT PARKING LOT', 'AIRCRAFT', 'AIRPORT EXTERIOR - NON-SECURE AREA',
       'POOL ROOM', 'FIRE STATION', 'VEHICLE - OTHER RIDE SERVICE']

crime_type = ['THEFT', 'BATTERY', 'CRIMINAL DAMAGE', 'NARCOTICS', 'ASSAULT',
       'OTHER OFFENSE', 'BURGLARY', 'MOTOR VEHICLE THEFT',
       'DECEPTIVE PRACTICE', 'ROBBERY', 'CRIMINAL TRESPASS',
       'WEAPONS VIOLATION', 'PROSTITUTION', 'OFFENSE INVOLVING CHILDREN',
       'PUBLIC PEACE VIOLATION', 'CRIM SEXUAL ASSAULT', 'SEX OFFENSE',
       'INTERFERENCE WITH PUBLIC OFFICER', 'LIQUOR LAW VIOLATION', 'GAMBLING',
       'ARSON', 'KIDNAPPING', 'HOMICIDE', 'STALKING', 'INTIMIDATION',
       'OBSCENITY', 'CONCEALED CARRY LICENSE VIOLATION', 'NON-CRIMINAL',
       'PUBLIC INDECENCY', 'OTHER NARCOTIC VIOLATION', 'HUMAN TRAFFICKING',
       'NON - CRIMINAL', 'RITUALISM', 'NON-CRIMINAL (SUBJECT SPECIFIED)',
       'DOMESTIC VIOLENCE']

beat = [2535,  312, 1533,  735, 1024, 1713, 2011, 2525,  623, 1632,  523,
        313, 1831, 2234, 2033,  222,  813,  231, 2032,  533, 1922,  324,
        911, 1432, 1023, 1924, 1433,  233,  631,  812,  531,  914, 2523,
       1014,  224, 1131, 1531, 2534,  714,  633,  621,  912, 1121, 1031,
       1133, 1122, 1624,  232, 1824,  934, 1732, 1833, 1724,  311, 2023,
       1511, 1212, 1231, 2222,  331,  212,  411,  322,  726,  511,  414,
       2522, 1422, 1822, 1414,  234,  611, 1134, 1223, 1312, 2424,  634,
        923, 2422, 2512, 1522, 2022,  614, 1213,  933, 1424, 1834,  513,
       2233, 2413, 1034, 1135,  215, 2232, 2113, 1412, 2515,  214,  235,
        834, 1723,  524,  433,  124, 1332, 1423, 1931, 2112,  733,  612,
       1214, 1811, 2122,  134,  624,  825,  712, 1224, 1235, 2012,  835,
        431, 2533, 1921,  613, 1222, 1823,  922,  915, 1021, 1722, 1914,
        722, 1125,  532, 1523,  921,  422, 1731,  731,  811, 2511, 1911,
       1434, 1611,  112, 1132, 2131, 2521,  111, 2024, 1324,  132, 1633,
        223, 1215, 1233, 1234, 1532, 2532, 1232,  831, 1114,  913,  632,
        131, 1711,  423,  732,  412,  122,  823,  724, 1421, 1512,  931,
       1123,  421, 1631,  833,  424,  814,  113, 1933, 1934, 2423,  935,
       1524,  321, 1012, 2333,  725, 2411,  323, 1623,  815, 2111,  522,
       2123, 1712, 2433,  622,  432,  734, 1622,  932,  924, 1011, 1333,
       2531, 1431, 2211,  211, 1022, 1832,  832, 1211, 1113, 1111,  213,
        713, 2221, 1313,  925,  824, 1033, 2432, 2431, 1915,  711, 1634,
       2311,  114,  332, 1331,  715,  123,  333,  314, 1912,  821, 1733,
       1932, 1614, 2223, 1112, 2322, 2412, 1821, 1814, 1935, 1923, 2312,
        225, 1032, 2124, 2324, 2514, 2212,  413,  133, 2524, 1513,  221,
        434, 1013, 2031,  723, 1323, 1613,  512,  822, 1612, 1913, 1115,
       1925, 1124, 2313, 2331, 1413,  334, 1812, 1322, 1411, 2213,  121,
       1654, 2513, 1311, 1621, 2133, 1813, 2013, 1651, 1225, 2132, 2332,
       2323, 1221, 1653, 1655, 1652,  430]

hours = [i for i in range(0,24)]




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
    return render_template("crime/templates/MLform.html",location_list=location_list,hours=hours,crime_type=crime_type,beat=beat)

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
