# 1. import Flask
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, inspect, func, desc
from sqlalchemy import distinct
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify
import os.path


# 2. Create an app, being sure to pass __name__
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

Base.classes.keys()
measurement = Base.classes.measurement
station = Base.classes.station
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    
    return (
     f"Welcome to the Climate API<br/>"
     f"/api/v1.0/precipitation<br/>"
     f"/api/v1.0/stations<br/>"
     f"/api/v1.0/tobs<br/>"
     f"/api/v1.0/YYYY-MM-DD<br/>"
     f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"

    )
# 4. Define what to do when a user hits the /about route
@app.route("//api/v1.0/precipitation")
def rain():
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    one_year =session.query(measurement.date,measurement.prcp).\
        filter(measurement.date > year_ago).\
        order_by(measurement.date).all()

    session.close()
    rain_dates = []
    for date, prcp in one_year:
        rain_dict={}
        rain_dict["date"]=date
        rain_dict["prcp"]=prcp
        rain_dates.append(rain_dict)
    return jsonify(rain_dates)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine) 

    station_name_count = session.query(station.name, func.count(measurement.station)).filter(measurement.station == station.station)\
    .group_by(measurement.station).all()
    station_name_count
    
    
    station_list = list(np.ravel(station_name_count))

    session.close()
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():    
    session = Session(engine) 
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365) 
    
    hist_data =session.query(measurement.tobs).\
    filter(measurement.date >= year_ago).\
    filter(measurement.station == 'USC00519281').all()

    tobs = list(np.ravel(hist_data))

    session.close()

    return jsonify(tobs)


@app.route("/api/v1.0/<start_date>")
def start(start_date):    
    session = Session(engine) 
    temps =session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).all()
    
    
    session.close()
    return jsonify(temps)

@app.route("/api/v1.0/<start_date>/<end_date>")
def range(start_date,end_date):    
    session = Session(engine) 
    temps =session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
 
   
    session.close()

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)