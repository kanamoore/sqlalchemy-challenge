from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home page. List all routes that are available.
@app.route("/")
def home():
    return (f"Available routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/startdate<br/>"
            f"/api/v1.0/startdate/enddate")

# Convert the query results to a Dictionary using date as the key and prcp as the value.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    prcp_data = session.query(Measurement.date, Measurement.prcp).all()
    dict_prcp = dict(prcp_data)
    session.close()
    return jsonify(dict_prcp)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.station).all()
    session.close()
    return jsonify(stations)


# Query for the dates and temperature observations from a year from the last data point.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= "2016-08-23").all()
    session.close()
    return jsonify(tobs)

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    min_temperature = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).all()
    avg_temperature = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    max_temperature = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    session.close()

    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # return jsonify(start, min_temperature, avg_temperature, max_temperature)

    return (f"After {start} : <br/>"
            f"Min temperature was {min_temperature} (F) <br/>"
            f"Max temperature was {max_temperature} (F) <br/>"
            f"Average temperature is {avg_temperature} (F) ")
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date,  the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    min_temperature = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    avg_temperature = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    max_temperature = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
    # return jsonify(start, end, min_temperature, avg_temperature, max_temperature)
    return (f"Between {start} and {end} : <br/>"
            f"Min temperature was {min_temperature} (F) <br/>"
            f"Average temperature was {avg_temperature} (F) <br/>"
            f"Max temperature was {max_temperature} (F)")
    
# Hints
# You will need to join the station and measurement tables for some of the analysis queries.

if __name__ == '__main__':
    app.run(debug=True)


