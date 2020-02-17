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
@app.route("/")
def home():
    return (f"Available routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/startdate<br/>"
            f"/api/v1.0/startdate/enddate")

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
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


# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.
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
    temperature = session.query(Measurement.tobs).filter(Measurement.date >= start).all()

    session.close()
    min_temperature = min(temperature)
    # avg_temperature = sum(temperature) / len(temperature)
    max_temperature = max(temperature)
    return jsonify(start, min_temperature, max_temperature)
    # return jsonify({f"After{start}, min temperature was {min_temperature} max temperature was {max_temperature}"})
        
    # print(f"Min temperature was {min_temperature}")
    # print(f"Max temperature was {max_temperature}")
    
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    temperature = session.query(Measurement.tobs).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    min_temperature = min(temperature)
    # avg_temperature = sum(temperature) / len(temperature)
    max_temperature = max(temperature)

    session.close()
    return jsonify(start, end, min_temperature, max_temperature)
    
# Hints
# You will need to join the station and measurement tables for some of the analysis queries.

if __name__ == '__main__':
    app.run(debug=True)


