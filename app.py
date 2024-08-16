# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os
import datetime as dt
import numpy as np
#################################################
# Database Setup
#################################################
path = os.path.join('Resources', 'hawaii.sqlite')
engine = create_engine(f"sqlite:///{path}")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurements = base.classes.measurement
stations = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# some extra stuff for a more accurate date
recentdate = session.query(func.max(measurements.date)).first()

# Calculate the date one year from the last date in data set.
recentdatestr = recentdate[0]
# 2016 was a leap year
previousYear = (dt.datetime.strptime(recentdatestr, '%Y-%m-%d') - dt.timedelta(days=366)).replace(
    year=(dt.datetime.strptime(recentdatestr, '%Y-%m-%d')).year - 1)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)
@app.route('/')
def home():
    return(
        f'<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>'
        f'<center><h3>Select from the available options:</h3></center>'
        f'<center>/api/v1.0/precipitation</center>'
        f'<center>/api/v1.0/station</center>'
        f'<center>/api/v1.0/tobs</center>'
        f'<center>/api/v1.0/start</center>'
        f'<center>/api/v1.0/start/end</center>'
    )




#################################################
# Flask Routes
#################################################
# /api/v1.0/precipitation route
@app.route('/api/v1.0/precipitation')
def precip():
    # create previous year's precipitation as a json


    # Perform a query to retrieve the data and precipitation scores
    results = session.query(measurements.date, measurements.prcp).filter(measurements.date >= previousYear).all()

    session.close()
    # dictionary with data as key and precipitation as the value
    precipitation = {date: prcp for date, prcp in results}
    # convert to a json
    return jsonify(precipitation)
    # closing the query session
    session.close()

# /api/v1.0/station route
@app.route('/api/v1.0/station')
def station():
    # list of stations
    # query to retrieve names of stations
    results = session.query(stations.station).all()
    # closing the query session
    session.close()

    # convert to list
    stationList = list(np.ravel(results))
    # to .JSON
    return jsonify(stationList)

# /api/v1.0/tobs route
@app.route('/api/v1.0/tobs')
def temperatures():
    # bring in the data from the past year, from the most recent data point.
    results = session.query(
        measurements.date,
        measurements.tobs  # Use 'tobs' here instead of 'temperature'
    ).filter(measurements.station == 'USC00519281').filter(measurements.date >= previousYear).all()
    session.close()
    # Convert to list
    tempList = []
    for row in results:
        # Create a dictionary with date and temperature values
        temp_dict = {
            'date': row[0],
            'temperature': row[1]
        }
        tempList.append(temp_dict)

    # to .JSON
    return jsonify(tempList)

# /api/v1.0/start/end and /api/v.10/start
@app.route('/api/v1.0/<start>')
@app.route('/api/v1.0/<start>/<end>')
def dateStats(start=None, end=None):

    # select
    selections = [func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)]
    # creating a reference point for the start date and end date of the data collection
    startDate = dt.datetime.strptime(start, '%m%d%Y')
    endDate = dt.datetime.strptime(end, '%m%d%Y')
    if not end:
        # for grabing data from a certain timepoint all the way to the most recent timepoint
        results = session.query(*selections).filter(measurements.date >= startDate).all()
        session.close()
        # Convert to list
        tempList = list(np.ravel(results))
        # to .JSON
        return jsonify(tempList)

    else:
        # for grabing data between two timepoints
        results = session.query(*selections).filter(measurements.date >= startDate).filter(measurements.date <= endDate).all()
        session.close()
        # Convert to list
        tempList = list(np.ravel(results))
        # to .JSON
        return jsonify(tempList)
# launcher
if __name__ == '__main__':
    app.run(debug=True)
