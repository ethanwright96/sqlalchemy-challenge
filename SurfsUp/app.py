import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to the table(s)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes

# Home Page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available API Routes:<br/><br/>"
        f"Precipitation (2016-08-23 - 2017-08-23):   /api/v1.0/precipitation<br/><br/>"
        f"List of All Stations:   /api/v1.0/stations<br/><br/>"
        f"Temperature Recordings (2016-08-23 - 2017-08-23) at Most Active Station:   /api/v1.0/tobs<br/><br/>"
        f"Enter Start Date (YYYY-MM-DD) for Temperature Summary:   /api/v1.0/<start><br/><br/>"
        f"Enter Start and End Date (YYYY-MM-DD) for Temperature Summary:   /api/v1.0/<start>/<end><br/><br/>"
        f"For more information on API Calls, please contact ethan@harvestintelligence.net. Thank you!"
    )

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Define the start of the period of interest
    period_start = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query date and prcp for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= period_start).\
                order_by(Measurement.date).all()
    
    # Close session
    session.close()
    
    # Convert results to dictionary
    results_dict = dict(results)
    
    # Return jsonified data
    return jsonify(results_dict)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
    
    # Query all stations
    results = session.query(Station.station).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    list_stations = list(np.ravel(results))

    return jsonify(list_stations)

# TOBS Route
@app.route("/api/v1.0/tobs")
def tobs():
    # Query stations and count ids to find, group_by, and order_by activity level
    station_activity = session.query(Measurement.station, func.count(Measurement.id)).\
    group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()

    # Save the most active station
    most_active_station = station_activity[0][0]
    
    # Define the start of the period of interest
    period_start = dt.date(2017,8,23) - dt.timedelta(days=365)
    
    # Query the dates and temperature of the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == most_active_station).filter(Measurement.date >= period_start).all()
    
    # Close session
    session.close()
    
    # Append results to empty list as dictionaries
    data = []
    for date, tobs in results:
        results_dict = {}
        results_dict["date"] = date
        results_dict["tobs"] = tobs
        data.append(results_dict)

    # Return list of dictionaries with results
    return jsonify(data)

# Start Route
@app.route("/api/v1.0/<start>")
def start(start):
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    # Close session
    session.close()
    
    # Create an empty list to hold dictionaries
    results_list = []
    
    # Write for loop to append summary stat dictionaries to list
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        results_list.append(tobs_dict)
        
    # Return list of dictionaries with results    
    return jsonify(results_list)

# Start-End Route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                func.max(Measurement.tobs)).filter(Measurement.date >= start).\
                                    filter(Measurement.date <= end).all()
    
    session.close()
    
    results_list = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        results_list.append(tobs_dict)
        
    return jsonify(results_list)

# Close session
session.close()

# Turn on Flask's debug mode
if __name__ == '__main__':
    app.run(debug=True)

