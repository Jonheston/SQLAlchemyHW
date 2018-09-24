
# import dependencies 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy


engine = create_engine("sqlite:///Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"- List of prior year rain totals from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"- List of Station numbers and names<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"- List of prior year temperatures from all stations<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"- When given the start date (YYYY-MM-DD), calculates the MIN/AVG/MAX temperature for all dates greater than and equal to the start date<br/>"
        f"<br/>"
        f"/api/v1.0/start/end<br/>"
        f"- When given the start and the end date (YYYY-MM-DD), calculate the MIN/AVG/MAX temperature for dates between the start and end date inclusive<br/>"

    )
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    today = dt.date(2017,8,23)
    year_ago = today - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `prcp` as the keys and values
    precipitation_data = []
    for result in precipitation:
        row = {}
        row["date"] = precipitation[0]
        row["prcp"] = precipitation[1]
        precipitation_data.append(row)

    return jsonify(precipitation_data)

#########################################################################################
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
   stations = session.query(Station.name, Station.station)
   stations_df = pd.read_sql(stations.statement, stations.session.bind)
   return jsonify(stations_df.to_dict())


#########################################################################################
#Return a JSON list of Temperature Observations (tobs) for the previous year.


@app.route("/api/v1.0/tobs")
def tobs():
    today = dt.date(2017,8,23)
    year_ago = today - dt.timedelta(days=365)
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()

    temperatures = []
    for result in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temperatures.append(row)

    return jsonify(temperatures)
#########################################################################################
#@app.route("/api/v1.0/<start>")
#def trip1(start):

 # go back one year from start date and go to end of data for Min/Avg/Max temp   
#    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
#    last_year = dt.timedelta(days=365)
#    start = start_date-last_year
#    end =  dt.date(2017, 8, 23)
#    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
#        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
#    trip = list(np.ravel(trip_data))
#    return jsonify(trip)

#########################################################################################
#@app.route("/api/v1.0/<start>/<end>")
#def trip2(start,end):

  # go back one year from start/end date and get Min/Avg/Max temp     
#    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
#    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
#    last_year = dt.timedelta(days=365)
#    start = start_date-last_year
#    end = end_date-last_year
#    trip_data = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
#        filter(Measurements.date >= start).filter(Measurements.date <= end).all()
#    trip = list(np.ravel(trip_data))
#    return jsonify(trip)

#########################################################################################

if __name__ == "__main__":
    app.run(debug=True)