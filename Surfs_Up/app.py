# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import numpy as np
import pandas as pd

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# create Flask app instance
app = Flask(__name__)

# create home page and list available routes
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # create session
    session = Session(engine)

    # calculate the date one year before August 23, 2017
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # query the precipitation data for the last year
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).all()

    # close session
    session.close()

    # create dictionary from the results and convert to JSON
    precipitation_data = {}
    for date, prcp in results:
        precipitation_data[date] = prcp
    return jsonify(precipitation_data)



@app.route("/api/v1.0/stations")
def stations():
    # create session
    session = Session(engine)

    # query all stations
    results = session.query(Station.station).all()

    # close session
    session.close()

    # convert list of tuples to list
    stations_list = list(result[0] for result in results)

    # return JSON list of stations
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations for the last year"""
    session = Session(engine)
    # calculate the date 1 year ago from today
    today = dt.date(2017, 8, 23)
    last_year = today - dt.timedelta(days=365)
    # query for the temperature observations for the most active station for the last year
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()
    tobs_data = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station[0]).filter(Measurement.date >= last_year).all()
    session.close()
    # convert the query results to a list of dictionaries
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the start date string to a datetime object
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # Find the last date in the dataset
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    end_date = dt.datetime.strptime(last_date, '%Y-%m-%d')

    # Calculate the TMIN, TAVG, and TMAX for all dates greater than or equal to the start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries from the results and return as JSON
    start_temps = []
    for min_temp, avg_temp, max_temp in results:
        start_dict = {}
        start_dict["Minimum Temperature"] = min_temp
        start_dict["Average Temperature"] = round(avg_temp,2)
        start_dict["Maximum Temperature"] = max_temp
        start_temps.append(start_dict)

    return jsonify(start_temps)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Convert the start and end date strings to datetime objects
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Calculate the TMIN, TAVG, and TMAX for dates between the start and end date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    # Close the session
    session.close()

    # Create a list of dictionaries from the results and return as JSON
    start_end_temps = []
    for min_temp, avg_temp, max_temp in results:
        start_end_dict = {}
        start_end_dict["Minimum Temperature"] = min_temp
        start_end_dict["Average Temperature"] = round(avg_temp,2)
        start_end_dict["Maximum Temperature"] = max_temp
        start_end_temps.append(start_end_dict)

    return jsonify(start_end_temps)


if __name__ == '__main__':
    app.run(debug=True)