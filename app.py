# Import the dependencies.
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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
        f'<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>'
        f'<center><h3>Select from the available options:</h3></center>'
        f'<center>/api/v1.0/precipitation</center>'
        f'<center>/api/v1.0/stations</center>'
        f'<center>/api/v1.0/tobs</center>'
        f'<center>/api/v1.0/start</center>'
        f'<center>/api/v1.0/start/end</center>'
    )


# launcher
if __name__ == '__main__':
    app.run(debug=True)
