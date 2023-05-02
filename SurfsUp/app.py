# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
# reflect the tables
# Save references to each table
# Create our session (link) from Python to the DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measures = Base.classes.measurement
Station = Base.classes.station
sessions1 = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Homepage
@app.route("/")
def welcome():
    return """
    
<html>
<h1><center>List Of All Available Routes<br></h1></center>
<center><img src="https://www.lovebigisland.com/wp-content/uploads/MeanRFAnn_Hawaii_in.jpg" height="75%" width="50%"/><br><br>
<p>Precipitation Route</p>
<li><a href="/api/v1.0/precipitation">Precipitation Route</a></li><br>

<p>Stations Route</p>
<li><a href="/api/v1.0/stations">Stations Route</a></li><br>

<p>Tobs Route</p>
<li><a href="/api/v1.0/tobs">Tobs Route</a></li><br>

<p>Start Route</p>
<li><a href="/api/v1.0/2016-8-23">Start Route</a></li><br>

<p>Stop Route</p>
<li><a href="/api/v1.0/2016-8-23/2017-8-23">Stop Route</a></li><br>
</html>

"""

#Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
    Precipitation = dt.date(2017,8,23) - dt.timedelta(days=365)
    PrecipitationScores = sessions1.query(Measures.date, Measures.prcp).filter(Measures.date >= Precipitation).order_by(Measures.date).all()
    PrecipitationList = dict(PrecipitationScores)
    return jsonify(PrecipitationList)


#Stations Route
@app.route("/api/v1.0/stations")
def stations():
    stations1 = sessions1.query(Station.station).all()
    stationslist = list(np.ravel(stations1))
    return jsonify(stationslist)


#Tobs Route
@app.route("/api/v1.0/tobs")
def tobs():
    Precipitation = dt.date(2017,8,23) - dt.timedelta(days=365)
    Tobs = sessions1.query(Measures.tobs).filter(Measures.date >= Precipitation).order_by(Measures.date).all()
    TobsList = list(np.ravel(Tobs))
    return jsonify(TobsList)

#Start Route
@app.route("/api/v1.0/<start>")
def beginofday(start):
    beginofday = sessions1.query(Measures.date, func.min(Measures.tobs), func.avg(Measures.tobs), func.max(Measures.tobs)).filter(Measures.date >= start).all()
    beginninglist = list(np.ravel(beginofday))
    return jsonify(beginninglist)

#Stop Route
@app.route("/api/v1.0/<start>/<end>")
def endofday(start, end):
    endofday = sessions1.query(Measures.date, func.min(Measures.tobs), func.avg(Measures.tobs), func.max(Measures.tobs)).filter(Measures.date >= start).filter(Measures.date <= end).all()
    endofdaylist = list(np.ravel(endofday))
    return jsonify(endofdaylist)


if __name__ == '__main__':
    app.run(debug=True)