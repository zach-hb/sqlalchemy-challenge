# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with = engine)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

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
def homepage():
    """List all available routes"""
    
    return (
        f"Available Routes: <br/>"
        f"/api/v1.0/precipiation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipiation")
def precipitation():
    """Add query reults into a dictionary, then jsonify it."""

    results = session.query(measurement).filter(measurement.date >="2016-08-23")
    dates = []
    prcps = []
    for result in results:
        dates.append(result.date)
        prcps.append(result.prcp)
    dp_dict = dict(zip(dates, prcps))
    return jsonify(dp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations in json format."""
    
    stations_result = session.query(station.station).all()
    stations_list = []
    for result in stations_result:
        stations_list.append(result[0])
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return dates and temperature observations for most active station in json format."""

    temp_active = []
    ma_results = session.query(measurement).filter(measurement.station >="USC00519281")
    for i in ma_results:
        temp_active.append(i.tobs)
    return jsonify(temp_active)   


@app.route("/api/v1.0/<start>", methods = ['GET'])
def start(start):
    """Return JSON list of min, avg, and max temperature from a specified start date."""

    t_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs))\
    .filter(measurement.date >= start).all()
    
    return jsonify(t_results)


@app.route("/api/v1.0/<start>/<end>", methods = ['GET'])
def start_end(start,end):
    """Return JSON list of min, avg, and max temperature for a specified range of dates."""

    se_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
    .filter((measurement.date.between(start,end))).all()

    return jsonify(se_results)


if __name__ == '__main__':
    app.run(debug=True)