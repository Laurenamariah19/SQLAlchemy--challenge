# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return(
        f"Available Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>"
            )

@app.route('/api/v1.0/precipitation')
def precipitation():
    one_year = dt.date(2017,8,23)- dt.timedelta(days = 365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year).all()
    session.close()
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(station.station).all()
    session.close()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    one_year = dt.date(2017,8,23)- dt.timedelta(days = 365)
    results = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281', measurement.date >= one_year).all()
    session.close()
    tobs_list = [{date: tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route('/api/v1.0/<start>')
def start(start):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()
    session.close()
    return jsonify({
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    })

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    return jsonify({
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    })

if __name__ == "__main__":
    app.run()