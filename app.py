import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
 

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine,reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station



@app.route('/')
def home_page():
    return (
    	f"Home Page<br/>"
    	f"Available Routes:<br/>"
    	f"/api/v1.0/precipitation<br/>"
    	f"/api/v1.0/stations<br/>"
    	f"/api/v1.0/tobs<br/>"
    	f"/api/v1.0/start<br/>"
    	f"/api/v1.0/start/end")


@app.route('/api/v1.0/precipitation')
def precipitation():

	session = Session(engine)

	results = session.query(Measurement.date, Measurement.prcp).all()
		
	session.close()

	all_measurements = []

	for date, prcp in results:
		Measurement_dict = {}
		Measurement_dict["date"] = date
		Measurement_dict["prcp"] = prcp
		all_measurements.append(Measurement_dict)

	return jsonify(all_measurements)


@app.route('/api/v1.0/stations')
def stations():
	session = Session(engine)

	results = session.query(Station.station,Station.name).all()

	session.close()

	print(results)

	all_stations = list(np.ravel(results))

	return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
	session = Session(engine)

	year_before_most_recent_stationid = dt.date(2017,8,18) - dt.timedelta(days=365)

	results = session.query(Measurement.tobs).\
    	filter(Measurement.date >= year_before_most_recent_stationid).all()


	session.close()

	print(results)

	tobs = list(np.ravel(results))

	return jsonify(tobs)


@app.route("/api/v1.0/start")
def start():

	session = Session(engine) 
	start_date = dt.date(2010,1,1)
	sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
	results = session.query(*sel).filter(Measurement.date >= start_date).all()

	session.close()
	print(results)

	tobs_start = list(np.ravel(results))
	return jsonify(tobs_start)


@app.route('/api/v1.0/start/end')
def start_end():

	session = Session(engine)
	start_date = dt.date(2010,1,1)
	end_date = dt.date(2014,4,20)
	sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
	results = session.query(*sel).filter((Measurement.date > start_date) & (Measurement.date < end_date)).all()

	session.close()

	print(results)

	tobs_start_end = list(np.ravel(results))
	return jsonify(tobs_start_end)


if __name__ == "__main__":
    app.run(debug=True)
