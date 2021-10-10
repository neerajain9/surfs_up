# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Setup Database
##################
## Create engine
engine = create_engine("sqlite:///hawaii.sqlite")

## Reflect DB
Base = automap_base()

## Reflect Tables
Base.prepare(engine, reflect=True)

#Save Reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

## Create Session
session = Session(engine)
##################

# FLASK
## Create a New Flask App Instance
app = Flask(__name__)

## Create flask Routes
@app.route('/')
## Create a function for this route
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! \
    Available Routes: \
    /api/v1.0/precipitation \
    /api/v1.0/stations \
    /api/v1.0/tobs \
    /api/v1.0/temp/start/end \
    ''')
    return 

@app.route('/api/v1.0/precipitation')
## Create a function for this route
def precipitation():
    # Calculate date one year prior
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query to get the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()

    # Jsonify the output
    precip = {date: prcp for date, prcp in precipitation}
    session.close()
    return jsonify(precip)
    #return precip

@app.route('/api/v1.0/stations')
## Create a function for this route
def stations():
    # query to get stations
    results = session.query(Station.station).all()

    # unraveling results into a one-dimensional array
    stations = list(np.ravel(results))
    
    session.close()    
    # Jsonify the output
    ## refer https://flask.palletsprojects.com/en/1.1.x/api/#flask.json.jsonify
    return jsonify(STATIONS=stations)
    

@app.route('/api/v1.0/tobs')
## Create a function for this route
def temp_monthly():
    # Calculate date one year prior
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query to get the date and precipitation for the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()

    # unraveling results into a one-dimensional array
    temps = list(np.ravel(results))

    # Jsonify the output
    session.close()
    return jsonify(TEMPS=temps)


@app.route('/api/v1.0/temp/<start>/<end>')
## Create a function for this route
def stats(start=None, end=None):
    # # Calculate date one year prior
    # prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query to get the date and precipitation for the previous year
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        session.close()
        return jsonify(TEMPS=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    session.close()
    return jsonify(TEMPS=temps)
    