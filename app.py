import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

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

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:"
        '<ul>'
            f"<li><a href='/api/v1.0/precipitation'>Precipitation</a></li>"
            f"<li><a href='/api/v1.0/stations'>Stations</a></li>"
            f"<li><a href='/api/v1.0/tobs'>Temperatures</a></li>"
            f"<li><a href='/api/v1.0/<start'>Start</a></li>"
            f"<li><a href='/api/v1.0/<start>/<end'>Start End</a></li>"
        '</ul>'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date,Measurement.prcp).all()

    return jsonify( {date:precip for date,precip in prcp} )
   

@app.route("/api/v1.0/stations")
def stations():
     #Query stations
    stations = session.query(Station.station).all()

    return jsonify(total_stations)
    

@app.route("/api/v1.0/tobs")
def tobs():
     #Query the dates and temperature observations of the most 
     #active station for the last year of data

    #Temperature observations (TOBS) for the previous year
    lastYear = dt.date(2017,8,23) - dt.timedelta(days=365)

    temp = session.query(Measurement.tobs).filter(Measurement.date >= lastYear).all()

    return jsonify(temp)     
# 
#@app.route("/api/v1.0/<start")
#def start():
# 
# 
#@app.route("/api/v1.0/<start>/<end")
#def start>/<end():


if __name__ == '__main__':
    app.run(debug=True)
