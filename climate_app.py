# 1. import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt
from datetime import timedelta

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/start<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    # Query all precipitations
    results = session.query(Measurement.date, Measurement.prcp).all()

    #session.close()

    # Create a dictionary from the row data and append to a list of all_precipitations
    all_precipitations = []
    for date, prcp in results:
        precipitation_dict= {}
        precipitation_dict["Date"] = date
        precipitation_dict["Precipitation"] = prcp
        all_precipitations.append(precipitation_dict)

    session.close()

    return jsonify(all_precipitations)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all stations
    stations_names = session.query(Station.name).all()

    session.close()

    return jsonify(stations_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Query for the dates and temperature observations from a year from the last data point."""
    # Calculate the date 1 year ago from the last data point in the database
    last_date = session.query(Measurement).order_by(Measurement.date.desc()).first().date
    first_date = (pd.to_datetime(last_date) - timedelta(days=365)).date()

    # Perform a query to retrieve the data and temperatures for this period
    datas = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= first_date)
    temperatures=[]
    for date, tobs in datas:
        dict_temp = {}
        dict_temp["Date"] = date
        dict_temp["Temperature"] = tobs
        temperatures.append(dict_temp)
    session.close()

    return jsonify(temperatures)

@app.route("/api/v1.0/start<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start"""
    # Select the values for the query
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), 
   func.max(Measurement.tobs)]
    # Perform a query to retrieve the data and temperatures for this period
    start_temperatures = session.query(*sel).filter(Measurement.date >= start)

    tobs = []
    for tmin, tavg, tmax in start_temperatures:
        temp_dict= {}
        temp_dict["Temperature Min"] = tmin
        temp_dict["Temperature Avg"] = tavg
        temp_dict["Temperature Max"] = tmax
        tobs.append(temp_dict)

    session.close()


    return jsonify(tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a start-end"""
    # Select the values for the query
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), 
   func.max(Measurement.tobs)]
    # Perform a query to retrieve the data and temperatures for this period
    start_end_temperatures = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end)

    tobs = []
    for tmin, tavg, tmax in start_end_temperatures:
        temp_dict= {}
        temp_dict["Temperature Min"] = tmin
        temp_dict["Temperature Avg"] = tavg
        temp_dict["Temperature Max"] = tmax
        tobs.append(temp_dict)

    session.close()


    return jsonify(tobs)
   
if __name__ == "__main__":
    app.run(debug=True)